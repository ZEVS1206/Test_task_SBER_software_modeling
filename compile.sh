cd ChampSim
./config.sh champsim_config.json
make -j $(nproc)
cp bin/champsim bin/$1
cd ..

