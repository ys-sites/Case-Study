/**
 * Web Audio API synthesizer for tactile writing feedback and focus ambiance.
 * 100% client-side, zero external audio asset dependencies.
 */

class AudioEngine {
  private ctx: AudioContext | null = null;
  private rainSource: AudioBufferSourceNode | null = null;
  private rainGain: GainNode | null = null;
  private masterGain: GainNode | null = null;

  private init() {
    if (!this.ctx) {
      const AudioContextClass = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new AudioContextClass();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.value = 0.5;
      this.masterGain.connect(this.ctx.destination);
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  public setVolume(volume: number) {
    if (this.masterGain) {
      this.masterGain.gain.setValueAtTime(Math.max(0, Math.min(1, volume)), this.ctx?.currentTime || 0);
    }
  }

  /**
   * Synthesize mechanical typewriter key click
   */
  public playKeyClick(isSpace = false, isEnter = false) {
    try {
      this.init();
      if (!this.ctx || !this.masterGain) return;

      const now = this.ctx.currentTime;

      if (isEnter) {
        // Carriage return ding / mechanical clack
        const osc = this.ctx.createOscillator();
        const bellGain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1760, now); // High clean bell A6
        osc.frequency.exponentialRampToValueAtTime(1750, now + 0.4);

        bellGain.gain.setValueAtTime(0.18, now);
        bellGain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

        osc.connect(bellGain);
        bellGain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 0.5);
      }

      // Mechanical stroke noise burst
      const bufferSize = this.ctx.sampleRate * (isSpace ? 0.04 : 0.025);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.25));
      }

      const noise = this.ctx.createBufferSource();
      noise.buffer = buffer;

      // Filter to simulate hollow mechanical keycaps
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      const baseFreq = isSpace ? 800 : isEnter ? 1200 : 1600 + (Math.random() * 400 - 200);
      filter.frequency.setValueAtTime(baseFreq, now);
      filter.Q.setValueAtTime(2.5, now);

      const clickGain = this.ctx.createGain();
      const vol = isSpace ? 0.12 : isEnter ? 0.16 : 0.1 + Math.random() * 0.05;
      clickGain.gain.setValueAtTime(vol, now);
      clickGain.gain.exponentialRampToValueAtTime(0.001, now + (isSpace ? 0.04 : 0.03));

      noise.connect(filter);
      filter.connect(clickGain);
      clickGain.connect(this.masterGain);

      noise.start(now);
    } catch {
      // Audio playback fails gracefully if browser restricts
    }
  }

  /**
   * Gentle meditation chime for Pomodoro timer completion
   */
  public playChime() {
    try {
      this.init();
      if (!this.ctx || !this.masterGain) return;

      const now = this.ctx.currentTime;
      const freqs = [528, 792, 1056]; // Harmonics

      freqs.forEach((freq, idx) => {
        if (!this.ctx || !this.masterGain) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);

        const initialGain = 0.2 / (idx + 1);
        gain.gain.setValueAtTime(initialGain, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.2);

        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 2.5);
      });
    } catch {
      // Fail gracefully
    }
  }

  /**
   * Ambient focus rain sound generator
   */
  public startAmbientRain() {
    try {
      this.init();
      if (!this.ctx || !this.masterGain) return;
      this.stopAmbient();

      const sampleRate = this.ctx.sampleRate;
      const bufferLength = sampleRate * 2; // 2 seconds loop
      const buffer = this.ctx.createBuffer(1, bufferLength, sampleRate);
      const data = buffer.getChannelData(0);

      // Pink / brown noise approximation for soothing rain
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferLength; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.035;
        b6 = white * 0.115926;
      }

      this.rainSource = this.ctx.createBufferSource();
      this.rainSource.buffer = buffer;
      this.rainSource.loop = true;

      const lowpass = this.ctx.createBiquadFilter();
      lowpass.type = 'lowpass';
      lowpass.frequency.setValueAtTime(1400, this.ctx.currentTime);

      this.rainGain = this.ctx.createGain();
      this.rainGain.gain.setValueAtTime(0.12, this.ctx.currentTime);

      this.rainSource.connect(lowpass);
      lowpass.connect(this.rainGain);
      this.rainGain.connect(this.masterGain);

      this.rainSource.start();
    } catch {
      // Audio autoplay restrictions
    }
  }

  public stopAmbient() {
    if (this.rainSource) {
      try {
        this.rainSource.stop();
        this.rainSource.disconnect();
      } catch {
        // Ignored
      }
      this.rainSource = null;
    }
  }
}

export const soundEngine = new AudioEngine();
