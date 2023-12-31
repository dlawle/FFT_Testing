import pylab as pl
import scipy.io.wavfile as wf
import sys

"""
A pitch shifter with formant preservation is shown in Listing B.21. A version of
this program without this feature can be created by removing the spectral envelope
scaling factor in the phase vocoder synthesis method call. Its command line takes a
number for the pitch ratio and two files:
$ python3 pshift.py <ratio> input.wav output.wav

"""

def stft(x,w,n):
    N = len(w)
    X = pl.rfft(x*w)
    k = pl.arange(0,N/2+1)
    return X*pl.exp(-2*pl.pi*1j*k*n/N)

def istft(X,w,n):
    N = len(w)
    k = pl.arange(0,N/2+1)
    xn = pl.irfft(X*pl.exp(2*pl.pi*1j*k*n/N))
    return xn*w

def modpi(x):
    if x >= pl.pi: x -= 2*pl.pi
    if x < -pl.pi: x += 2*pl.pi
    return x

unwrap = pl.vectorize(modpi)

class Pvoc:
    def __init__(self,w,h,sr):
        N = len(w)
        self.win = w
        self.phs = pl.zeros(N//2+1)
        self.h = h
        self.n = 0
        self.fc = pl.arange(N//2+1)*sr/N
        self.sr = sr

    def analysis(self,x):
        X = stft(x,self.win,self.n)
        delta = pl.angle(X) - self.phs
        self.phs = pl.angle(X)
        delta = unwrap(delta)
        f = self.fc + delta*self.sr/(2*pl.pi*self.h)
        self.n += self.h
        return abs(X),f
    
    def synthesis(self,a,f):
        delta = (f - self.fc)*(2*pl.pi*self.h)/self.sr
        self.phs += delta
        X=a*pl.cos(self.phs) + 1j*a*pl.sin(self.phs)
        y = istft(X,self.win,self.n)
        self.n += self.h
        return y
    
N = 1024
D=8
H = N//D
zdbfs = 32768
(sr,signal) = wf.read(sys.argv[2])
signal = signal/zdbfs
L = len(signal)
output = pl.zeros(L)
win = pl.hanning(N)
pva = Pvoc(win,H,sr)
pvs = Pvoc(win,H,sr)
trans = float(sys.argv[1])

def scale(amps,freqs,p):
    N = len(freqs)
    a,f = pl.zeros(N),pl.zeros(N)
    for i in range(0, N):
        n = int((i*p))
    if n>0 and n < N-1:
        f[n] = p*freqs[i]
        a[n] = amps[i]
    return a,f

def true_spec_env(amps,coefs,thresh):
    N = len(amps)
    sm = 10e-15
    form = pl.zeros(N)
    lmags = pl.log(amps[:N-1]+sm)
    mags = lmags
    check = True

    while(check):
        ceps = pl.rfft(lmags)
        ceps[coefs:] = 0
        form[:N-1] = pl.irfft(ceps)

        for i in range(0,N-1):
            if lmags[i] < form[i]: lmags[i] = form[i]
            diff = mags[i] - form[i]
            if diff > thresh: check = True
            else: check = False

        return pl.exp(form)+sm
    
for n in range(0,L,H):
    if(L-n < N): break
    amps,freqs = pva.analysis(signal[n:n+N])
    env1 = true_spec_env(amps,40,0.23)
    amps,freqs = scale(amps,freqs,trans)
    env2 = true_spec_env(amps,40,0.23)
    output[n:n+N] += pvs.synthesis(amps*env1/env2,freqs)

scal = max(output)/max(signal)
output = pl.array(output*zdbfs/scal,dtype='int16')
wf.write(sys.argv[3],sr,output)