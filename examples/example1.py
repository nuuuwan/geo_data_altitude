def main():
    from alt_lk import Alt, LatLng

    latlng_sri_paada = LatLng(6.809498226498262, 80.49925188865949)
    alt = Alt.from_latlng(latlng_sri_paada)

    print(alt)
    print(alt.alt_m)
    print(alt.alt_ft)
    print(str(alt))

    latlng_piduruthalagala = LatLng(lat=7.001665, lng=80.772689)
    latlng_kirigalpotta = LatLng(lat=6.813, lng=80.783)
    latlng_thotapola = LatLng(lat=6.833, lng=80.82)

    alts = Alt.list_from_latlng_list(
        [
            latlng_piduruthalagala,
            latlng_kirigalpotta,
            latlng_thotapola,
        ]
    )

    for alt in alts:
        print(alt.alt_m)


if __name__ == '__main__':
    main()
