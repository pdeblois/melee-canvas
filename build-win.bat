call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
python build.py --generator "Visual Studio 17 2022" --variant RelWithDebInfo --cmake-vars ENABLE_NOGUI=OFF SLIPPI_PLAYBACK=false