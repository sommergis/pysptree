echo "Executing SWIG"
swig -c++ -python pySPTree.i
echo "Compiling"
python setup.py build_ext --inplace
