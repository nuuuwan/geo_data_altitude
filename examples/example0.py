if __name__ == '__main__':
    from alt_lk import Alt, LatLng

    latlng_sri_paada = LatLng(6.809498226498262, 80.49925188865949)
    alt = Alt.from_latlng(latlng_sri_paada)

    print(alt)
    print(alt.alt_m)
    print(alt.alt_ft)
    print(str(alt))
