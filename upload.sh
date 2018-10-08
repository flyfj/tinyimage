if [ -d "dist" ]; then
  rm -r dist
fi
python setup.py sdist bdist_wheel
# twine upload dist/*