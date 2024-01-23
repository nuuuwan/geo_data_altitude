from alt_lk import Alt, AltFile, GeoTIFFFile

if __name__ == '__main__':
    AltFile.list_from_dir_geotiff(GeoTIFFFile.DIR_GEO_TIF_ARC3)
    AltFile.list_from_dir_geotiff(GeoTIFFFile.DIR_GEO_TIF_ARC1)
    Alt.build_matrix()
