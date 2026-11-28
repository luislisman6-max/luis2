#!/bin/bash
# Construye un short: bash build.sh <render_pX.js> <salida.mp4> <inicio_voz_seg>
# Requiere WORK con voz.mp3 y tokens.json
set -euo pipefail
R=$1; OUTMP4=$2; VSTART=${3:-0}
cd "$(dirname "$0")"
: "${WORK:?WORK no definido}"
node "$R" meta > "$WORK/meta.txt"
python3 sfx_rdr.py "$WORK"
VCUT=$(awk '/^VCUT/{print $2}' "$WORK/meta.txt")
FR=$(awk '/^DUR/{print $4}' "$WORK/meta.txt"); DUR=$(awk '/^DUR/{print $2}' "$WORK/meta.txt")
P=4; STEP=$(( (FR + P - 1) / P ))
for i in $(seq 0 $((P-1))); do
  A=$((i*STEP)); B=$(( (i+1)*STEP ))
  node "$R" frames $A $B | ffmpeg -v error -y -f rawvideo -pix_fmt rgba -s 1080x1920 -r 30 -i - \
    -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p "$WORK/seg$i.mp4" &
done
wait
: > "$WORK/segs.txt"; for i in $(seq 0 $((P-1))); do echo "file '$WORK/seg$i.mp4'" >> "$WORK/segs.txt"; done
ffmpeg -v error -y -f concat -safe 0 -i "$WORK/segs.txt" -c copy "$WORK/video.mp4"
# voz recortada (empieza en VSTART) + efectos con ducking: la voz siempre manda
ffmpeg -v error -y -ss "$VSTART" -t "$VCUT" -i "$WORK/voz.mp3" -i "$WORK/sfx.wav" -filter_complex \
 "[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0,afade=t=out:st=$(python3 -c "print($VCUT-0.08)"):d=0.08,apad=whole_dur=$DUR,asplit[v][vk];\
  [1:a]volume=0.32[s];[s][vk]sidechaincompress=threshold=0.02:ratio=4:attack=5:release=300[sd];\
  [v][sd]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.0:LRA=11[a]" \
 -map "[a]" -c:a aac -b:a 192k -ar 44100 "$WORK/audio.m4a"
ffmpeg -v error -y -i "$WORK/video.mp4" -i "$WORK/audio.m4a" -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart "$OUTMP4"
ls -la "$OUTMP4"
