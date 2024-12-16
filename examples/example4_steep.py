import webbrowser


def main():
    import math

    from alt_lk import Alt

    MIN_STEEPNESS = 0.1
    MIN_DALT = 2000
    STEP = 10
    MAX_D = 1000
    [MIN_LAT, MAX_LAT, MIN_LNG, MAX_LNG] = [5.92, 9.83, 79.52, 81.88]

    m = Alt.matrix()
    nx = len(m)
    ny = len(m[0])
    print(f"nx={nx}, ny={ny}")
    info_idx = {}
    for i1 in range(0, nx, STEP):
        for j1 in range(0, ny, STEP):
            latlng1 = Alt.indices_to_latlng(i1, j1)

            if not (MIN_LAT <= latlng1.lat <= MAX_LAT):
                continue
            if not (MIN_LNG <= latlng1.lng <= MAX_LNG):
                continue

            alt1 = m[i1][j1]
            if alt1 < MIN_DALT:
                continue
            print(
                f"({i1/nx:.1%})",
                latlng1,
                end="\r",
            )

            for di in range(-MAX_D, MAX_D + STEP, STEP):
                i2 = i1 + di
                if not (0 <= i2 < nx):
                    continue
                for dj in range(-MAX_D, MAX_D + STEP, STEP):
                    j2 = j1 + dj
                    if i1 == i2 and j1 == j2:
                        continue
                    if not (0 <= j2 < ny):
                        continue
                    latlng2 = Alt.indices_to_latlng(i2, j2)

                    alt2 = m[i2][j2]
                    dalt = alt1 - alt2

                    if dalt < MIN_DALT:
                        continue

                    distance = latlng1.distance(latlng2) * 1_000

                    steepness = dalt / distance
                    if steepness < MIN_STEEPNESS:
                        continue
                    angle = math.atan2(dalt, distance) * 180 / math.pi

                    info = dict(
                        latlng1=latlng1,
                        latlng2=latlng2,
                        alt1=alt1,
                        alt2=alt2,
                        dalt=dalt,
                        distance=distance,
                        steepness=steepness,
                        angle=angle,
                    )
                    k = str(latlng1)
                    if k not in info_idx:
                        info_idx[k] = []
                    info_idx[k].append(info)

    info_idx = dict(
        sorted(
            [
                (
                    x[0],
                    sorted(
                        x[1], key=lambda info: info["steepness"], reverse=True
                    ),
                )
                for x in info_idx.items()
            ],
            key=lambda x: x[1][0]["steepness"],
            reverse=True,
        )
    )
    for info_list in info_idx.values():
        for info in info_list[:1]:
            latlng1 = info["latlng1"]
            latlng2 = info["latlng2"]
            alt1 = info["alt1"]
            alt2 = info["alt2"]
            dalt = info["dalt"]
            distance = info["distance"]
            steepness = info["steepness"]
            angle = info["angle"]

            print(
                f"{dalt:.0f}m",
                f"({alt1:.0f}m -> {alt2:.0f}m)",
                f"in {distance/1_000.0:.2f}km",
                f"at {steepness:.2f} ({angle:.2f}°)",
            )
            url1 = "https://www.google.com/maps/place" + f"/{latlng1}"
            url2 = "https://www.google.com/maps/place" + f"/{latlng2}"
            webbrowser.open(url1)
            webbrowser.open(url2)
            if input("Continue? (y/n): ") != "y":
                break


if __name__ == "__main__":
    main()
