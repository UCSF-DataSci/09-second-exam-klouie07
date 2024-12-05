python \generate_dirty_data.py

# Clean file
pip install numpy
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed 's/,,/,/g' > ms_data_cleaned.csv
cut -d',' -f1,2,4,5,6 ms_data_cleaned.csv > ms_data.csv
rm ms_data_cleaned.csv

# Set up insurance list
echo "Basic" > insurance.lst
echo "Average" >> insurance.lst
echo "Plus" >> insurance.lst
echo "Premium" >> insurance.lst

# Summary
wc -l ms_data.csv
head -n 10 ms_data.csv


