from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from alt_lk.data.JSONAltFile import JSONAltFile

if __name__ == '__main__':
    JSONAltFile.list_from_dir_geotiff(GeoTIFFFile.DIR_GEOTIFF)
    JSONAltFile.get_combined_data_for_lk()
