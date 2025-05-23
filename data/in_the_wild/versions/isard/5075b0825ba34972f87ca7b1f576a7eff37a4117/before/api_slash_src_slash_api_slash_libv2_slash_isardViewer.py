# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

#!/usr/bin/env python

import base64
import json
import os
import sys

from rethinkdb import RethinkDB

from api import app

from ..libv2.log import *

r = RethinkDB()
import urllib

from rethinkdb.errors import ReqlNonExistenceError

from ..libv2.flask_rethink import RDB
from .api_exceptions import Error

db = RDB(app)
db.init_app(app)

# from netaddr import IPNetwork, IPAddress

from datetime import datetime, timedelta

from jose import jwt

from ..libv2.apiv2_exc import *


def viewer_jwt(desktop_id, minutes=240):
    # user_id = provider_id+'-'+category_id+'-'+id+'-'+id
    return jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(minutes=minutes),
            "kid": "isardvdi-viewer",
            "data": {"desktop_id": desktop_id},
        },
        app.ram["secrets"]["isardvdi"]["secret"],
        algorithm="HS256",
    )


class isardViewer:
    def __init__(self):
        # Offset from base_port == spice
        self.spice = 0
        self.spice_tls = 1
        self.vnc = 2
        self.vnc_tls = 3
        self.vnc_ws = -198  # 5900-200????
        self.rdpgw_port = os.environ.get("VIEWER_RDPGW", 9999)
        pass

    def viewer_data(
        self,
        id,
        protocol="browser-vnc",
        default_viewer=False,
        get_cookie=True,
        get_dict=False,
        domain=False,
        user_id=False,
    ):
        if not domain:
            try:
                with app.app_context():
                    domain = (
                        r.table("domains")
                        .get(id)
                        .pluck("id", "name", "status", "viewer", "options", "user")
                        .run(db.conn)
                    )
            except ReqlNonExistenceError:
                raise Error("not_found", "Unable to get viewer for inexistent desktop")

        if not protocol in ["file-spice", "browser-vnc"] and not domain["status"] in [
            "Started",
            "Shutting-down",
        ]:
            raise Error(
                "precondition_required", "Unable to get viewer for non started desktop"
            )

        if (
            "preferred" not in domain["options"]["viewers"].keys()
            or not domain["options"]["viewers"]["preferred"] == default_viewer
        ):
            with app.app_context():
                r.table("domains").get(id).update(
                    {"options": {"viewers": {"preferred": default_viewer}}}
                ).run(db.conn)

        ### File viewers
        if protocol == "file-spice":
            port = domain["viewer"]["base_port"] + self.spice_tls
            vmPort = domain["viewer"].get("spice_ext_port", "80")
            consola = self.get_spice_file(domain, vmPort, port)
            return {
                "kind": "file",
                "protocol": "spice",
                "name": "isard-spice",
                "ext": consola[0],
                "mime": consola[1],
                "content": consola[2],
            }

        if protocol == "file-vnc":
            raise Error("not_found", "Viewer protocol not implemented")

        if protocol == "file-rdpvpn":
            return {
                "kind": "file",
                "protocol": "rdpvpn",
                "name": "isard-rdp-vpn",
                "ext": "rdp",
                "mime": "application/x-rdp",
                "content": self.get_rdp_file(domain["viewer"]["guest_ip"]),
            }

        if protocol == "file-rdpgw":
            return {
                "kind": "file",
                "protocol": "rdpgw",
                "name": "isard-rdp-gw",
                "ext": "rdp",
                "mime": "application/x-rdp",
                "content": self.get_rdp_gw_file(
                    domain["viewer"]["guest_ip"],
                    domain["viewer"]["static"],
                    self.rdpgw_port,
                    viewer_jwt(domain["id"], minutes=30),
                ),
            }

        ## Browser viewers
        if protocol == "browser-spice":
            data = {
                "vmName": domain["name"],
                "vmHost": domain["viewer"]["proxy_hyper_host"],
                "vmPort": str(domain["viewer"]["base_port"] + self.spice),
                "host": domain["viewer"]["proxy_video"],
                "port": domain["viewer"].get("html5_ext_port", "443"),
                "token": domain["viewer"]["passwd"],
            }
            cookie = base64.b64encode(
                json.dumps({"web_viewer": data}).encode("utf-8")
            ).decode("utf-8")
            uri = "https://" + domain["viewer"]["static"] + "/viewer/spice-web-client/"
            urlp = (
                "https://"
                + domain["viewer"]["static"]
                + "/viewer/spice-web-client/?vmName="
                + urllib.parse.quote_plus(domain["name"])
                + "&vmHost="
                + domain["viewer"]["proxy_hyper_host"]
                + "&host="
                + domain["viewer"]["proxy_video"]
                + "&vmPort="
                + data["port"]
                + "&passwd="
                + domain["viewer"]["passwd"]
            )
            return {
                "kind": "browser",
                "protocol": "spice",
                "viewer": uri,
                "urlp": urlp,
                "cookie": cookie,
                "values": data,
            }

        if protocol == "browser-vnc":
            data = {
                "vmName": domain["name"],
                "vmHost": domain["viewer"]["proxy_hyper_host"],
                "vmPort": str(domain["viewer"]["base_port"] + self.vnc),
                "host": domain["viewer"]["proxy_video"],
                "port": domain["viewer"].get("html5_ext_port", "443"),
                "token": domain["viewer"]["passwd"],
            }
            cookie = base64.b64encode(
                json.dumps({"web_viewer": data}).encode("utf-8")
            ).decode("utf-8")
            uri = "https://" + domain["viewer"]["static"] + "/viewer/noVNC/"
            urlp = (
                "https://"
                + domain["viewer"]["static"]
                + "/viewer/noVNC/?vmName="
                + urllib.parse.quote_plus(domain["name"])
                + "&vmHost="
                + domain["viewer"]["proxy_hyper_host"]
                + "&host="
                + domain["viewer"]["proxy_video"]
                + "&port="
                + data["port"]
                + "&vmPort="
                + data["vmPort"]
                + "&passwd="
                + domain["viewer"]["passwd"]
            )
            return {
                "kind": "browser",
                "protocol": "vnc",
                "viewer": uri,
                "urlp": urlp,
                "cookie": cookie,
                "values": data,
            }

        if protocol == "browser-rdp":
            data = {
                "vmName": domain["name"],
                "vmHost": domain["viewer"]["guest_ip"],
                "vmUsername": domain["options"]["credentials"]["username"]
                if "credentials" in domain["options"]
                else "",
                "vmPassword": domain["options"]["credentials"]["password"]
                if "credentials" in domain["options"]
                else "",
                "host": domain["viewer"]["proxy_video"],
                "port": domain["viewer"].get("html5_ext_port", "443"),
            }
            cookie = base64.b64encode(
                json.dumps({"web_viewer": data}).encode("utf-8")
            ).decode("utf-8")
            uri = (f"https://{domain['viewer']['static']}/Rdp",)
            urlp = "Not implemented"
            return {
                "kind": "browser",
                "protocol": "rdp",
                "viewer": uri,
                "urlp": urlp,
                "cookie": cookie,
                "values": data,
            }

        if protocol == "vnc-client-macos":
            raise Error("not_found", "Viewer protocol not implemented")

        return ViewerProtocolNotFound

    def get_rdp_file(self, ip):
        ## This are the default values dumped from a windows rdp client connection to IsardVDI
        # connection type:i:7
        # networkautodetect:i:1
        # bandwidthautodetect:i:1
        # displayconnectionbar:i:1
        # username:s:
        # enableworkspacereconnect:i:0
        # disable wallpaper:i:0
        # allow font smoothing:i:0
        # allow desktop composition:i:0
        # disable full window drag:i:1
        # disable menu anims:i:1
        # disable themes:i:0
        # disable cursor setting:i:0
        # bitmapcachepersistenable:i:1
        # audiomode:i:0
        # redirectprinters:i:1
        # redirectcomports:i:0
        # redirectsmartcards:i:1
        # redirectclipboard:i:1
        # redirectposdevices:i:0
        # drivestoredirect:s:
        # autoreconnection enabled:i:1
        # authentication level:i:2
        # prompt for credentials:i:0
        # negotiate security layer:i:1
        # remoteapplicationmode:i:0
        # alternate shell:s:
        # shell working directory:s:
        # gatewayhostname:s:
        # gatewayusagemethod:i:4
        # gatewaycredentialssource:i:4
        # gatewayprofileusagemethod:i:0
        # promptcredentialonce:i:0
        # gatewaybrokeringtype:i:0
        # use redirection server name:i:0
        # rdgiskdcproxy:i:0
        # kdcproxyname:s:
        return """full address:s:%s
""" % (
            ip
        )

    def get_rdp_gw_file(self, ip, proxy_video, proxy_port, jwt_token):
        return """full address:s:%s
gatewayhostname:s:%s:%s
gatewaycredentialssource:i:5
gatewayusagemethod:i:1
gatewayprofileusagemethod:i:1
gatewayaccesstoken:s:%s
networkautodetect:i:1
bandwidthautodetect:i:1
connection type:i:6
username:s:
domain:s:
bitmapcachesize:i:32000
smart sizing:i:1""" % (
            ip,
            proxy_video,
            proxy_port,
            jwt_token,
        )

    def get_spice_file(self, domain, port, vmPort):
        op_fscr = int(
            domain.get("options", {})
            .get("viewers", {})
            .get("spice", {})
            .get("fullscreen", False)
        )
        c = "%"
        consola = """[virt-viewer]
        type=%s
        proxy=http://%s:%s
        host=%s
        password=%s
        tls-port=%s
        fullscreen=%s
        title=%s:%sd - Prem SHIFT+F12 per sortir
        enable-smartcard=0
        enable-usb-autoshare=1
        delete-this-file=1
        usb-filter=-1,-1,-1,-1,0
        tls-ciphers=DEFAULT
        """ % (
            "spice",
            domain["viewer"]["proxy_video"],
            port,
            domain["viewer"]["proxy_hyper_host"],
            domain["viewer"]["passwd"],
            vmPort,
            op_fscr,
            domain["name"] + " (TLS)",
            c,
        )

        consola = (
            consola
            + """%shost-subject=%s
        %sca=%r
        toggle-fullscreen=shift+f11
        release-cursor=shift+f12
        secure-attention=ctrl+alt+end
        secure-channels=main;inputs;cursor;playback;record;display;usbredir;smartcard"""
            % (
                "" if domain["viewer"]["tls"]["host-subject"] is not False else ";",
                domain["viewer"]["tls"]["host-subject"],
                "" if domain["viewer"]["tls"]["certificate"] is not False else ";",
                domain["viewer"]["tls"]["certificate"],
            )
        )

        consola = consola.replace("'", "")
        return "vv", "application/x-virt-viewer", consola

    ##### VNC NOT DONE

    def get_domain_vnc_data(self, domain, hostnames, viewer, port):
        try:
            cookie = base64.b64encode(
                json.dumps(
                    {
                        "web_viewer": {
                            "host": hostnames["host"],
                            "port": str(int(port)),
                            "token": domain["viewer"]["passwd"],
                        }
                    }
                ).encode("utf-8")
            ).decode("utf-8")

            return {
                "uri": "https://" + hostnames["proxy"] + "/static/noVNC",
                "cookie": cookie,
            }

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.error(exc_type, fname, exc_tb.tb_lineno)
            log.error("Viewer for domain " + domain["name"] + " exception:" + str(e))
            return False

    # ~ def get_domain_vnc_data(self, domain, hostnames, viewer, port, tlsport, selfsigned, remote_addr=False):
    # ~ try:
    # ~ ''' VNC does not have ssl. Only in websockets is available '''
    # ~ if viewer['defaultMode'] == "Secure" and domain['viewer']['port_spice_ssl'] is not False:
    # ~ return {'host':hostname,
    # ~ 'name': domain['name'],
    # ~ 'port': port,
    # ~ 'wsport': str(int(port)+500),
    # ~ 'ca':viewer['certificate'],
    # ~ 'domain':viewer['domain'],
    # ~ 'host-subject':viewer['host-subject'],
    # ~ 'passwd': domain['viewer']['passwd'],
    # ~ 'uri': 'https://<domain>/wsviewer/novnclite'+selfsigned+'/?host='+hostname+'&port='+str(int(port))+'&password='+domain['viewer']['passwd'],
    # ~ 'options': domain['options']['viewers']['vnc'] if 'vnc' in domain['options']['viewers'].keys() else False}
    # ~ if viewer['defaultMode'] == "Insecure" and domain['viewer']['port_spice'] is not False:
    # ~ return {'host':hostname,
    # ~ 'name': domain['name'],
    # ~ 'port': port,
    # ~ 'wsport': str(int(port)+500),
    # ~ 'ca':viewer['certificate'],
    # ~ 'domain':viewer['domain'],
    # ~ 'host-subject':viewer['host-subject'],
    # ~ 'passwd': domain['viewer']['passwd'],
    # ~ 'uri': 'http://<domain>/wsviewer/novnclite/?host='+hostname+'&port='+str(int(port))+'&password='+domain['viewer']['passwd'],
    # ~ 'options': domain['options']['viewers']['vnc'] if 'vnc' in domain['options']['viewers'].keys() else False}
    # ~ log.error('No available VNC Viewer for domain '+domain['name']+' exception:'+str(e))
    # ~ return False
    # ~ except Exception as e:
    # ~ exc_type, exc_obj, exc_tb = sys.exc_info()
    # ~ fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    # ~ log.error(exc_type, fname, exc_tb.tb_lineno)
    # ~ log.error('Viewer for domain '+domain['name']+' exception:'+str(e))
    # ~ return False

    ##### VNC FILE VIEWER
    def get_vnc_file(self, dict, id, clientos, remote_addr=False):
        ## Should check if ssl in use: dict['tlsport']:
        hostname = dict["host"]
        # ~ if dict['tlsport']:
        # ~ return False
        # ~ os='MacOS'
        if clientos in ["iOS", "Windows", "Android", "Linux", "generic", None]:
            consola = """[Connection]
            Host=%s
            Port=%s
            Password=%s

            [Options]
            UseLocalCursor=1
            UseDesktopResize=1
            FullScreen=1
            FullColour=0
            LowColourLevel=0
            PreferredEncoding=ZRLE
            AutoSelect=1
            Shared=0
            SendPtrEvents=1
            SendKeyEvents=1
            SendCutText=1
            AcceptCutText=1
            Emulate3=1
            PointerEventInterval=0
            Monitor=
            MenuKey=F8
            """ % (
                hostname,
                dict["port"],
                dict["passwd"],
            )
            consola = consola.replace("'", "")
            return "vnc", "text/plain", consola

        if clientos in ["MacOS"]:
            vnc = (
                "vnc://"
                + hostname
                + ":"
                + dict["passwd"]
                + "@"
                + hostname
                + ":"
                + dict["port"]
            )
            consola = """<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>URL</key>
                <string>%s</string>
                <key>restorationAttributes</key>
                <dict>
                    <key>autoClipboard</key>
                    <false/>
                    <key>controlMode</key>
                    <integer>1</integer>
                    <key>isFullScreen</key>
                    <false/>
                    <key>quality</key>
                    <integer>3</integer>
                    <key>scalingMode</key>
                    <true/>
                    <key>screenConfiguration</key>
                    <dict>
                        <key>GlobalIsMixedMode</key>
                        <false/>
                        <key>GlobalScreen</key>
                        <dict>
                            <key>Flags</key>
                            <integer>0</integer>
                            <key>Frame</key>
                            <string>{{0, 0}, {1920, 1080}}</string>
                            <key>Identifier</key>
                            <integer>0</integer>
                            <key>Index</key>
                            <integer>0</integer>
                        </dict>
                        <key>IsDisplayInfo2</key>
                        <false/>
                        <key>IsVNC</key>
                        <true/>
                        <key>ScaledSelectedScreenRect</key>
                        <string>(0, 0, 1920, 1080)</string>
                        <key>Screens</key>
                        <array>
                            <dict>
                                <key>Flags</key>
                                <integer>0</integer>
                                <key>Frame</key>
                                <string>{{0, 0}, {1920, 1080}}</string>
                                <key>Identifier</key>
                                <integer>0</integer>
                                <key>Index</key>
                                <integer>0</integer>
                            </dict>
                        </array>
                    </dict>
                    <key>selectedScreen</key>
                    <dict>
                        <key>Flags</key>
                        <integer>0</integer>
                        <key>Frame</key>
                        <string>{{0, 0}, {1920, 1080}}</string>
                        <key>Identifier</key>
                        <integer>0</integer>
                        <key>Index</key>
                        <integer>0</integer>
                    </dict>
                    <key>targetAddress</key>
                    <string>%s</string>
                    <key>viewerScaleFactor</key>
                    <real>1</real>
                    <key>windowContentFrame</key>
                    <string>{{0, 0}, {1829, 1029}}</string>
                    <key>windowFrame</key>
                    <string>{{45, 80}, {1829, 1097}}</string>
                </dict>
            </dict>
            </plist>""" % (
                vnc,
                vnc,
            )
            consola = consola.replace("'", "")
            return "vncloc", "text/plain", consola
