import math
from typing import Literal

import mapbox_vector_tile
from asyncpg import Connection
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from shapely.geometry import Point, Polygon

from modules import query, tiles
from modules.dependencies import database
from modules.params import Params

router = APIRouter()


def _errors_mvt(
    results,
    z: int,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    limit: int,
):
    if not results or len(results) == 0:
        return None
    else:
        limit_feature = []
        if len(results) == limit and z < 18:
            limit_feature = [
                {
                    "name": "limit",
                    "features": [
                        {
                            "geometry": Point(
                                (min_lon + max_lon) / 2, (min_lat + max_lat) / 2
                            )
                        }
                    ],
                }
            ]

        issues_features = []
        for res in sorted(results, key=lambda res: -res["lat"]):
            issues_features.append(
                {
                    "geometry": Point(res["lon"], res["lat"]),
                    "properties": {
                        "uuid": res["uuid"],
                        "item": res["item"] or 0,
                        "class": res["class"] or 0,
                    },
                }
            )

        return mapbox_vector_tile.encode(
            [{"name": "issues", "features": issues_features}] + limit_feature,
            quantize_bounds=(min_lon, min_lat, max_lon, max_lat),
        )


def _errors_geojson(
    results,
    z: int,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    limit: int,
):
    if not results or len(results) == 0:
        return None
    else:
        issues_features = []
        for res in sorted(results, key=lambda res: -res["lat"]):
            issues_features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(res["lon"]), float(res["lat"])],
                    },
                    "properties": {
                        "uuid": res["uuid"],
                        "item": res["item"] or 0,
                        "class": res["class"] or 0,
                    },
                }
            )

        features_collection = {
            "type": "FeatureCollection",
            "features": issues_features,
        }

        if len(results) == limit and z < 18:
            features_collection["properties"] = {"limit": limit}

        return features_collection


@router.get("/0.3/issues/{z}/{x}/{y}.heat.mvt", tags=["tiles"])
async def heat(
    request: Request, z: int, x: int, y: int, db: Connection = Depends(database.db)
):
    COUNT = 32

    lon1, lat2 = tiles.tile2lonlat(x, y, z)
    lon2, lat1 = tiles.tile2lonlat(x + 1, y + 1, z)

    params = Params(request)
    items = query._build_where_item(params.item, "items")
    params.tilex = x
    params.tiley = y
    params.zoom = z

    if params.zoom > 18:
        return

    limit = await db.fetchrow(
        """
SELECT
    SUM((SELECT SUM(t) FROM UNNEST(number) t))
FROM
    items
WHERE
"""
        + items
    )
    if limit and limit[0]:
        limit = float(limit[0])
    else:
        raise HTTPException(status_code=404)

    join, where, sql_params = query._build_param(
        await db,
        None,
        params.source,
        params.item,
        params.level,
        params.users,
        params.classs,
        params.country,
        params.useDevItem,
        params.status,
        params.tags,
        params.fixable,
        tilex=params.tilex,
        tiley=params.tiley,
        zoom=params.zoom,
    )

    sql_params += [lon1, lat1, lon2, lat2, COUNT]
    sql = (
        f"""
SELECT
    COUNT(*),
    (
        (lon-${len(sql_params)-4}) * ${len(sql_params)} /
            (${len(sql_params)-2}-${len(sql_params)-4}) + 0.5
    )::int AS latn,
    (
        (lat-${len(sql_params)-3}) * ${len(sql_params)} /
            (${len(sql_params)-1}-${len(sql_params)-3}) + 0.5
    )::int AS lonn,
    mode() WITHIN GROUP (ORDER BY items.marker_color) AS color
FROM
"""
        + join
        + """
WHERE
"""
        + where
        + """
GROUP BY
    latn,
    lonn
"""
    )

    features = []
    for row in await db.fetch(
        sql,
    ):
        count, x, y, color = row
        count = max(
            int(
                math.log(count)
                / math.log(limit / ((z - 4 + 1 + math.sqrt(COUNT)) ** 2))
                * 255
            ),
            1 if count > 0 else 0,
        )
        if count > 0:
            count = 255 if count > 255 else count
            features.append(
                {
                    "geometry": Polygon(
                        [(x, y), (x - 1, y), (x - 1, y - 1), (x, y - 1)]
                    ),
                    "properties": {"color": int(color[1:], 16), "count": count},
                }
            )

    return Response(
        content=mapbox_vector_tile.encode(
            [{"name": "issues", "features": features}], extents=COUNT
        ),
        media_type="application/vnd.mapbox-vector-tile",
    )


TileFormat = Literal["mvt", "geojson"]


@router.get("/0.3/issues/{z}/{x}/{y}.{format}", tags=["tiles"])
async def issues_mvt(
    request: Request,
    z: int,
    x: int,
    y: int,
    format: TileFormat,
    db: Connection = Depends(database.db),
):
    lon1, lat2 = tiles.tile2lonlat(x, y, z)
    lon2, lat1 = tiles.tile2lonlat(x + 1, y + 1, z)

    params = Params(request, max_limit=50 if z > 18 else 10000)
    params.tilex = x
    params.tiley = y
    params.zoom = z
    params.full = False

    if params.zoom > 18:
        return
    if (not params.users) and (not params.source) and (params.zoom < 7):
        return

    results = await query._gets(db, params) if z >= 7 else None

    if format == "mvt":
        tile = _errors_mvt(results, z, lon1, lat1, lon2, lat2, params.limit)
        if tile:
            return Response(
                content=tile, media_type="application/vnd.mapbox-vector-tile"
            )
        else:
            return Response(
                status_code=204, media_type="application/vnd.mapbox-vector-tile"
            )
    elif format in ("geojson", "json"):  # Fall back to GeoJSON
        tile = _errors_geojson(results, z, lon1, lat1, lon2, lat2, params.limit)
        if tile:
            return Response(content=tile, media_type="application/vnd.geo+json")
        else:
            return Response(content=[], media_type="application/vnd.geo+json")
    else:
        raise HTTPException(status_code=404)
