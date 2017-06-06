set PATH=./;c:/radiance/bin.
set RAYPATH=./;c:/radiance/lib.
dxdaylight C:/STADIC/Mistrick_Stadic_Example.json > out.txt
copy C:\STADIC\res\intermediateData\*.sig C:\STADIC\res\*.sig
dxprocessshade C:/STADIC/Mistrick_Stadic_Example.json
copy C:\STADIC\res\Classroom1_final.ill C:\STADIC\res\Classroom1.ill
dxmetrics C:/STADIC/Mistrick_Stadic_Example.json
