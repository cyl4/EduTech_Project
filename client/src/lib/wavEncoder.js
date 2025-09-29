export function encodeWAV(arrayBuffer, sampleRate = 48000, numChannels = 1) {
  const bytesPerSample = 2; // 16-bit audio
  const blockAlign = numChannels * bytesPerSample;
  const byteRate = sampleRate * blockAlign;
  const dataLength = arrayBuffer.byteLength;
  const wavBuffer = new ArrayBuffer(44 + dataLength);
  const view = new DataView(wavBuffer);

  // RIFF header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + dataLength, true); // File size - 8 bytes
  writeString(view, 8, 'WAVE');

  // fmt subchunk
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true); // Subchunk size
  view.setUint16(20, 1, true); // Audio format (1 = PCM)
  view.setUint16(22, numChannels, true); // Number of channels
  view.setUint32(24, sampleRate, true); // Sample rate
  view.setUint32(28, byteRate, true); // Byte rate
  view.setUint16(32, blockAlign, true); // Block align
  view.setUint16(34, bytesPerSample * 8, true); // Bits per sample

  // data subchunk
  writeString(view, 36, 'data');
  view.setUint32(40, dataLength, true); // Data size
  new Uint8Array(wavBuffer, 44).set(new Uint8Array(arrayBuffer)); // PCM data

  return new Blob([wavBuffer], { type: 'audio/wav' });
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}