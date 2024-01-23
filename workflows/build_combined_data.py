from alt_lk import Alt
from alt_lk.data.AltFile import AltFile
from alt_lk.data.GeoTIFFFile import GeoTIFFFile

if __name__ == '__main__':
    AltFile.list_from_dir_geotiff(GeoTIFFFile.DIR_ALT_TIF)
    Alt.build_combined_data_file()
