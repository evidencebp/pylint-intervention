import copy
import numpy
from .gqrs import time_to_sample_number, Conf, Peak, Annotation

def find_peaks(x):
    # Definitions:
    # * Hard peak: a peak that is either /\ or \/
    # * Soft peak: a peak that is either /-*\ or \-*/ (In that cas we define the middle of it as the peak)

    # Returns two numpy arrays:
    # * hard_peaks contains the indexes of the Hard peaks
    # * soft_peaks contains the indexes of the Soft peaks

    if len(x) == 0:
        return numpy.empty([0]), numpy.empty([0])

    tmp = x[1:]
    tmp = numpy.append(tmp, [x[-1]])
    tmp = x-tmp
    tmp[numpy.where(tmp>0)] = +1
    tmp[numpy.where(tmp==0)] = 0
    tmp[numpy.where(tmp<0)] = -1
    tmp2 = tmp[1:]
    tmp2 = numpy.append(tmp2, [0])
    tmp = tmp-tmp2
    hard_peaks = numpy.where(numpy.logical_or(tmp==-2,tmp==+2))[0]+1
    soft_peaks = []
    for iv in numpy.where(numpy.logical_or(tmp==-1,tmp==+1))[0]:
        t = tmp[iv]
        i = iv+1
        while True:
            if i==len(tmp) or tmp[i] == -t or tmp[i] == -2 or tmp[i] == 2:
                break
            if tmp[i] == t:
                soft_peaks.append(int(iv+(i-iv)/2))
                break
            i += 1
    soft_peaks = numpy.asarray(soft_peaks)+1
    return hard_peaks, soft_peaks


class GQRS(object):
    def putann(self, annotation):
        self.annotations.append(copy.deepcopy(annotation))

    def detect(self, x, freq, adczero, threshold=1.0):
        self.c = Conf(ADC_units=1.0, freq=freq)
        self.annotations = []
        self.sample_valid = False

        if freq < 50:
            print("Sampling frequency is too low!")
            return

        if len(x) < 1:
            return []

        self.x = x
        self.freq = freq
        self.adczero = adczero

        self.qfv = numpy.zeros((self.c._BUFLN))
        self.smv = numpy.zeros((self.c._BUFLN))
        self.v1 = 0

        t0 = 0
        tf = len(x)-1
        self.t = 0 - self.c.dt4

        self.annot = Annotation(0, "NOTE", 0, 0)
        self.putann(self.annot)

        # Cicular buffer of Peaks
        first_peak = Peak(0,0,0)
        tmp = first_peak
        for _ in range(1, self.c._NPEAKS):
            tmp.next_peak = Peak(0,0,0)
            tmp.next_peak.prev_peak = tmp
            tmp = tmp.next_peak
        tmp.next_peak = first_peak
        first_peak.prev_peak = tmp
        self.current_peak = first_peak

        if self.c.spm > self.c._BUFLN:
            if tf - t0 > self.c._BUFLN:
                tf_learn = t0 + self.c._BUFLN - self.c.dt4
            else:
                tf_learn = tf - self.c.dt4
        else:
            if tf - t0 > self.c.spm:
                tf_learn = t0 + self.c.spm - self.c.dt4
            else:
                tf_learn = tf - self.c.dt4

        self.state = "LEARNING"
        self.gqrs(t0, tf_learn)

        self.rewind_gqrs()

        self.state = "RUNNING"
        t = t0 - self.c.dt4
        self.gqrs(t0, tf)

    def rewind_gqrs(self):
        self.countdown = -1
        self.annot.time = 0
        self.annot.type = "NORMAL"
        self.annot.subtype = 0
        self.annot.num = 0
        p = self.current_peak
        for _ in range(self.c._NPEAKS):
            p.time = 0
            p.type = 0
            p.amp = 0
            p = p.next_peak

    def at(self, t):
        if t < 0:
            self.sample_valid = False
            return None
        if t > len(self.x)-1:
            self.sample_valid = False
            return None
        return self.x[t]


    def smv_at(self, t):
        return self.smv[t&(self.c._BUFLN-1)]

    def smv_put(self, t, v):
        self.smv[t&(self.c._BUFLN-1)] = v

    def qfv_at(self, t):
        return self.qfv[t&(self.c._BUFLN-1)]

    def qfv_put(self, t, v):
        self.qfv[t&(self.c._BUFLN-1)] = v

    def sm(self, t): # CHECKED!
        # implements a trapezoidal low pass (smoothing) filter
        # (with a gain of 4*smdt) applied to input signal sig
        # before the QRS matched filter qf().
        # Before attempting to 'rewind' by more than BUFLN-smdt
        # samples, reset smt and smt0.
        smt = self.c.smt
        smdt = self.c.smdt

        while self.t > smt:
            smt += 1
            if smt > smt0:
                self.smv_put(smt, self.smv_at(smt-1) +\
                                self.at(smt+smdt) + self.at(smt+smdt-1) -\
                                self.at(smt-smdt) + self.at(smt-smdt-1))
            else:
                for j in range(1, smdt):
                    v = self.at(smt) + self.at(smt+j) + self.at(smt-j)
                self.smv_put(smt, (v << 1) + self.at(smt+j) + self.at(smt-j) -\
                                self.adczero * (smdt << 2))
        self.c.smt = smt

        return self.smv_at(t)

    def qf(self, t): # CHECKED!
        # evaluate the QRS detector filter for the next sample

        bufln = self.c._BUFLN - 1

        # do this first, to ensure that all of the other smoothed values needed below are in the buffer
        dv2 = self.sm(t + self.c.dt4) - self.smv_at(t-self.c.dt4)
        dv1 = self.smv_at(t+self.c.dt) - self.smv_at(t-self.c.dt)
        dv = dv1 << 1
        dv -= self.smv_at(t+self.c.dt2) - self.smv_at(t-self.c.dt2)
        dv = dv << 1
        dv += dv1
        dv -= self.smv_at(t+self.c.dt3) - self.smv_at(t-self.c.dt3)

        dv -= self.smv_at(t+self.c.dt3) - self.smv_at(t-self.c.dt3)
        dv = dv << 1
        dv += dv2
        self.v1 += dv
        v0 = self.v1 / self.c.v1norm
        self.qfv_put(t, v0*v0)

    def gqrs(self, from_sample, to_sample):
        self.countdown = -1

        c = None
        i = None
        qamp = None
        q0 = None
        q1 = 0
        q2 = 0
        rr = None
        rrd = None
        rt = None
        rtd = None
        rtdmin = None

        p = None # (Peak)
        q = None # (Peak)
        r = None # (Peak)
        tw = None # (Peak)

        last_peak = from_sample
        last_qrs = from_sample

        def add_peak(peak_time, peak_amp, type):
            p = self.current_peak.next_peak
            p.time = peak_time
            p.amp = peak_amp
            p.type = type
            self.current_peak = p
            p.next_peak.amp = 0

        def peaktype(p):
            # peaktype() returns 1 if p is the most prominent peak in its neighborhood, 2
            # otherwise.  The neighborhood consists of all other peaks within rrmin.
            # Normally, "most prominent" is equivalent to "largest in amplitude", but this
            # is not always true.  For example, consider three consecutive peaks a, b, c
            # such that a and b share a neighborhood, b and c share a neighborhood, but a
            # and c do not; and suppose that amp(a) > amp(b) > amp(c).  In this case, if
            # there are no other peaks, a is the most prominent peak in the (a, b)
            # neighborhood.  Since b is thus identified as a non-prominent peak, c becomes
            # the most prominent peak in the (b, c) neighborhood.  This is necessary to
            # permit detection of low-amplitude beats that closely precede or follow beats
            # with large secondary peaks (as, for example, in R-on-T PVCs).
            if p.type: # TODO: check that
                return p.type
            else:
                a = p.amp
                t0 = p.time - self.c.rrmin
                t1 = p.time + self.c.rrmin

                if t0 < 0:
                    t0 = 0

                pp = p.prev_peak
                while t0 < pp.time and pp.time < pp.next_peak.time:
                    if pp.amp == 0:
                        break
                    if a < pp.amp and peaktype(pp) == 1:
                        p.type = 2
                        return p.type
                    # end:
                    pp = pp.prev_peak

                pp = p.next_peak
                while pp.time < t1 and pp.time > pp.prev_peak.time:
                    if pp.amp == 0:
                        break
                    if a < pp.amp and peaktype(pp) == 1:
                        p.type = 2
                        return p.type
                    # end:
                    pp = pp.next_peak

                p.type = 1
                return p.type

        def find_missing(r, p):
            if r is None or p is None:
                return None

            minrrerr = p.time - r.time

            s = None
            q = r.next_peak
            while q.time < p.time:
                if peaktype(q) == 1:
                    rrtmp = q.time - r.time
                    rrerr = rrtmp - self.c.rrmean
                    if rrerr < 0:
                        rrerr = -rrerr
                    if rrerr < minrrerr:
                        minrrerr = rrerr
                        s = q
                # end:
                q = q.next_peak

            return s

        r = None
        next_minute = 0
        minutes = 0
        while self.t <= to_sample + self.c.sps:
            if self.countdown < 0:
                if self.sample_valid:
                    self.qf()
                else:
                    self.countdown = time_to_sample_number(1, self.freq)
                    self.state = "CLEANUP"
            else:
                self.countdown -= 1
                if self.countdown < 0:
                    break

            q0 = self.qfv_at(self.t)
            q1 = self.qfv_at(self.t-1)
            q2 = self.qfv_at(self.t-2)

            if q1 > self.c.pthr and q2 < q1 and q1 >= q0 and t > self.c.dt4:
                add_peak(self.t-1, q1, 0)
                last_peak = self.t-1

                p = self.current_peak.next
                while p.time < t-self.c.rtmax:
                    if p.time >= self.annot.time + self.c.rrmin and peaktype(p) == 1:
                        if p.amp > self.c.qthr:
                            rr = p.time - self.annot.time
                            q = find_missing(r, p)
                            if rr > self.c.rrmean + 2 * self.c.rrdev and\
                               rr > 2 * (self.c.rrmean - self.c.rrdev) and\
                               q is not None:
                                p = q
                                rr = p.time - self.annot.time
                                annot.subtype = 1
                            rrd = rr - self.c.rrmean
                            if rrd < 0:
                                rrd = -rrd
                            self.c.rrdev += (rrd - self.c.rrdev) >> 3
                            if rrd > self.c.rrinc:
                                rrd = self.c.rrinc
                            if rr > self.c.rrmean:
                                self.c.rrmean += rrd
                            else:
                                self.c.rrmean -= rrd
                            if p.amp > self.c.qthr * 4:
                                self.c.qthr += 1
                            elif p.amp < self.c.qthr:
                                self.c.qthr -= 1
                            if self.c.qthr > self.c.pthr * 20:
                                self.c.qthr = self.c.pthr * 20
                            last_qrs = p.time

                            if state == "RUNNING":
                                self.annot.time = p.time - self.c.dt2
                                self.annot.type = "NORMAL"
                                qsize = p.amp * 10.0 / self.c.qthr
                                if qsize > 127:
                                    qsize = 127
                                self.annot.num = qsize
                                putann(self.annot)
                                self.annot.time += self.c.dt2

                            # look for this beat's T-wave
                            tw = None
                            rtdmin = self.c.rtmean
                            q = p.next
                            while q.time > self.annot.time:
                                rt = q.time - self.annot.time - self.c.dt2
                                if rt < self.c.rtmin:
                                    continue
                                if rt > self.c.rtmax:
                                    break
                                rtd = rt - self.c.rtmean
                                if rtd < 0:
                                    rtd = -rtd
                                if rtd < rtdmin:
                                    rtdmin = rtd
                                    tw = q
                                # end:
                                q = q.next
                            if tw is not None:
                                tmp_time = tw.time - self.c.dt2
                                tann = Annotation(tmp_time, "TWAVE", 1 if tmp_time > self.annot.time + self.c.rtmean else 0, rtdmin)
                                if state == "RUNNING":
                                    putann(tann)
                                rt = tann.time - self.annot.time
                                self.c.rtmean += (rt - self.c.rtmean) >> 4
                                if self.c.rtmean > self.c.rtmax:
                                    self.c.rtmean = self.c.rtmax
                                elif self.c.rtmean < self.c.rtmin:
                                    self.c.rtmean = self.c.rrmin
                                tw.type = 2 # mark T-wave as secondary
                            r = p
                            q = None
                            qamp = 0
                            self.annot.subtype = 0
                        elif t - last_qrs > self.c.rrmax and self.c.qthr > self.c.qthmin:
                            self.c.qthr -= (self.c.qthr >> 4)
            elif t - last_qrs > self.c.rrmax and self.c.pthr > self.c.pthmin:
                self.c.pthr -= (self.c.pthr >> 4)

            t += 1
            if t >= next_minute:
                next_minute += self.c.spm
                minutes += 1
                if minutes >= 60:
                    minutes = 0

        if self.state == "LEANING":
            return

        # Mark the last beat or two.
        p = self.current_peak.next_peak
        while p.time < p.next_peak.time:
            if p.time >= self.annot.time + self.c.rrmin and p.time < tf and peaktype(p) == 1:
                self.annot.type = "NORMAL"
                self.annot.time = p.time
                putann(self.annot)
            # end:
            p = p.next_peak
