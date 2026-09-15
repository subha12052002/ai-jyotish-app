(function () {
    "use strict";

    /*
     * AI Jyotish — Chart Rendering Utilities
     *
     * This file only handles frontend chart visualization.
     * All planetary calculations continue to come from the backend.
     */

    const ZODIAC_SIGNS = [
        {
            name: "Aries",
            short: "Ar",
            symbol: "♈"
        },
        {
            name: "Taurus",
            short: "Ta",
            symbol: "♉"
        },
        {
            name: "Gemini",
            short: "Ge",
            symbol: "♊"
        },
        {
            name: "Cancer",
            short: "Cn",
            symbol: "♋"
        },
        {
            name: "Leo",
            short: "Le",
            symbol: "♌"
        },
        {
            name: "Virgo",
            short: "Vi",
            symbol: "♍"
        },
        {
            name: "Libra",
            short: "Li",
            symbol: "♎"
        },
        {
            name: "Scorpio",
            short: "Sc",
            symbol: "♏"
        },
        {
            name: "Sagittarius",
            short: "Sg",
            symbol: "♐"
        },
        {
            name: "Capricorn",
            short: "Cp",
            symbol: "♑"
        },
        {
            name: "Aquarius",
            short: "Aq",
            symbol: "♒"
        },
        {
            name: "Pisces",
            short: "Pi",
            symbol: "♓"
        }
    ];

    /*
     * Readable labels are used instead of Unicode astrological glyphs.
     * Glyphs such as ☿/♃ can render very small or differently across fonts.
     */
    const PLANET_SYMBOLS = {
        Sun: "Sun",
        Moon: "Moon",
        Mars: "Mars",
        Mercury: "Merc",
        Jupiter: "Jup",
        Venus: "Ven",
        Saturn: "Sat",
        Rahu: "Rahu",
        Ketu: "Ketu",
        Ascendant: "Asc"
    };

    const PLANET_NAMES = [
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "Rahu",
        "Ketu"
    ];

    function escapeHTML(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function number(value, fallback = 0) {
        const n = Number(value);
        return Number.isFinite(n) ? n : fallback;
    }
function normalizeSignIndex(value) {
    const n = Number(value);

    if (!Number.isFinite(n)) {
        return null;
    }

    /*
     * Backend sign_index is ZERO-BASED:
     * 0 = Aries
     * 1 = Taurus
     * 2 = Gemini
     * 3 = Cancer
     * 4 = Leo
     * 5 = Virgo
     * ...
     * 11 = Pisces
     */
    if (Number.isInteger(n) && n >= 0 && n <= 11) {
        return n;
    }

    return null;
}

    function getSignIndex(planet) {
        if (!planet) return null;

        const candidates = [
            planet.sign_index,
            planet.signIndex,
            planet.rashi_index,
            planet.rashiIndex,
            planet.signNumber,
            planet.sign_no,
            planet.zodiac_index
        ];

        for (const candidate of candidates) {
            const index =
                normalizeSignIndex(candidate);

            if (index !== null) {
                return index;
            }
        }

        const signText = String(
            planet.sign ||
            planet.rashi ||
            planet.zodiac ||
            ""
        ).trim().toLowerCase();

        if (!signText) return null;

        return ZODIAC_SIGNS.findIndex(
            (sign) =>
                sign.name.toLowerCase() === signText ||
                sign.short.toLowerCase() === signText
        );
    }

    function getHouse(planet) {
        if (!planet) return null;

        const candidates = [
            planet.house,
            planet.house_number,
            planet.houseNumber,
            planet.bhava
        ];

        for (const candidate of candidates) {
            const n = Number(candidate);

            if (
                Number.isFinite(n) &&
                n >= 1 &&
                n <= 12
            ) {
                return n;
            }
        }

        return null;
    }

    function getLongitude(planet) {
        if (!planet) return null;

        const candidates = [
            planet.longitude,
            planet.longitude_deg,
            planet.absolute_longitude,
            planet.absoluteLongitude,
            planet.degree_longitude
        ];

        for (const candidate of candidates) {
            const n = Number(candidate);

            if (Number.isFinite(n)) {
                return n;
            }
        }

        return null;
    }

    function getDegree(planet) {
        if (!planet) return null;

        const candidates = [
            planet.degree,
            planet.degrees,
            planet.degree_in_sign,
            planet.degreeInSign,
            planet.position
        ];

        for (const candidate of candidates) {
            const n = Number(candidate);

            if (
                Number.isFinite(n) &&
                n >= 0 &&
                n < 30
            ) {
                return n;
            }
        }

        const longitude =
            getLongitude(planet);

        if (longitude !== null) {
            return ((longitude % 30) + 30) % 30;
        }

        return null;
    }

    function getPlanetName(planet, fallback = "") {
        if (typeof planet === "string") {
            return planet;
        }

        return (
            planet?.name ||
            planet?.planet ||
            planet?.body ||
            fallback
        );
    }

    function getPlanets(chart) {
        if (!chart) return [];

        let source =
            chart.planets ||
            chart.planet_positions ||
            chart.planetPositions ||
            chart.bodies ||
            chart.analysis?.planets ||
            [];

        if (
            source &&
            !Array.isArray(source) &&
            typeof source === "object"
        ) {
            return Object.entries(source).map(
                ([name, value]) => ({
                    ...(typeof value === "object"
                        ? value
                        : { value }),
                    name:
                        value?.name ||
                        value?.planet ||
                        name
                })
            );
        }

        if (!Array.isArray(source)) {
            return [];
        }

        return source.map((planet) => {
            if (typeof planet === "string") {
                return {
                    name: planet
                };
            }

            return planet;
        });
    }

    function findPlanet(chart, name) {
        const normalized =
            String(name).toLowerCase();

        return getPlanets(chart).find(
            (planet) =>
                getPlanetName(
                    planet
                ).toLowerCase() === normalized
        );
    }

    function getAscendant(chart) {
        if (!chart) return null;

        return (
            chart.ascendant ||
            chart.asc ||
            chart.lagna ||
            chart.calculation?.ascendant ||
            chart.details?.ascendant ||
            null
        );
    }

    function getAscendantSign(chart) {
        const asc =
            getAscendant(chart);

        if (!asc) return null;

        if (typeof asc === "number") {
            return normalizeSignIndex(asc);
        }

        return getSignIndex(asc);
    }

    function getHouseSign(
        ascendantSign,
        house
    ) {
        if (
            ascendantSign === null ||
            !house
        ) {
            return null;
        }

        return (
            (ascendantSign +
                house -
                1) %
            12
        );
    }

    /*
     * ------------------------------------------
     * North Indian Kundli chart
     * ------------------------------------------
     */

  function createNorthIndianSVG(chart, options = {}) {

    const showAscendant =
        options.showAscendant !== false;

    const size = 720;
    const svgNS = "http://www.w3.org/2000/svg";

    const ascSign = getAscendantSign(chart);

    /*
     * ==========================================
     * CREATE 12 HOUSES
     * ==========================================
     */

    const houses = Array.from(
        { length: 12 },
        (_, index) => {

            const house = index + 1;

            return {
                house: house,

                sign:
                    ascSign === null
                        ? null
                        : getHouseSign(
                            ascSign,
                            house
                        ),

                planets: []
            };
        }
    );

    /*
     * Put the actual backend-calculated
     * planets into their houses.
     */

    getPlanets(chart).forEach(
        (planet) => {

            const house =
                getHouse(planet);

            if (
                house &&
                houses[house - 1]
            ) {
                houses[
                    house - 1
                ].planets.push(
                    planet
                );
            }
        }
    );

    /*
     * ==========================================
     * CREATE SVG
     * ==========================================
     */

    const svg =
        document.createElementNS(
            svgNS,
            "svg"
        );

    svg.setAttribute(
        "viewBox",
        "0 0 720 720"
    );

    svg.setAttribute(
        "class",
        "north-indian-kundli cosmic-kundli"
    );

    /* Explicit size so the chart is visible in every chart container. */
    svg.setAttribute("width", "720");
    svg.setAttribute("height", "720");
    svg.style.display = "block";
    svg.style.width = "100%";
    svg.style.maxWidth = "500px";
    svg.style.height = "auto";

    svg.setAttribute(
        "role",
        "img"
    );

    svg.setAttribute(
        "aria-label",
        "North Indian Vedic Kundli"
    );

    /*
     * ==========================================
     * DEFINITIONS
     * ==========================================
     */

    const defs =
        document.createElementNS(
            svgNS,
            "defs"
        );

    /*
     * ------------------------------------------
     * Cosmic blue gradient
     * ------------------------------------------
     */

    const gradient =
        document.createElementNS(
            svgNS,
            "linearGradient"
        );

    gradient.setAttribute(
        "id",
        "kundliCosmicGradient"
    );

    gradient.setAttribute(
        "x1",
        "0%"
    );

    gradient.setAttribute(
        "y1",
        "0%"
    );

    gradient.setAttribute(
        "x2",
        "100%"
    );

    gradient.setAttribute(
        "y2",
        "100%"
    );

    const stop1 =
        document.createElementNS(
            svgNS,
            "stop"
        );

    stop1.setAttribute(
        "offset",
        "0%"
    );

    stop1.setAttribute(
        "stop-color",
        "#06183A"
    );

    const stop2 =
        document.createElementNS(
            svgNS,
            "stop"
        );

    stop2.setAttribute(
        "offset",
        "50%"
    );

    stop2.setAttribute(
        "stop-color",
        "#0A2A5C"
    );

    const stop3 =
        document.createElementNS(
            svgNS,
            "stop"
        );

    stop3.setAttribute(
        "offset",
        "100%"
    );

    stop3.setAttribute(
        "stop-color",
        "#031027"
    );

    gradient.appendChild(stop1);
    gradient.appendChild(stop2);
    gradient.appendChild(stop3);

    defs.appendChild(
        gradient
    );

    /*
     * ------------------------------------------
     * Blue glow
     * ------------------------------------------
     */

    const filter =
        document.createElementNS(
            svgNS,
            "filter"
        );

    filter.setAttribute(
        "id",
        "kundliBlueGlow"
    );

    filter.setAttribute(
        "x",
        "-50%"
    );

    filter.setAttribute(
        "y",
        "-50%"
    );

    filter.setAttribute(
        "width",
        "200%"
    );

    filter.setAttribute(
        "height",
        "200%"
    );

    const blur =
        document.createElementNS(
            svgNS,
            "feGaussianBlur"
        );

    blur.setAttribute(
        "stdDeviation",
        "2.5"
    );

    blur.setAttribute(
        "result",
        "blur"
    );

    const merge =
        document.createElementNS(
            svgNS,
            "feMerge"
        );

    const blurNode =
        document.createElementNS(
            svgNS,
            "feMergeNode"
        );

    blurNode.setAttribute(
        "in",
        "blur"
    );

    const sourceNode =
        document.createElementNS(
            svgNS,
            "feMergeNode"
        );

    sourceNode.setAttribute(
        "in",
        "SourceGraphic"
    );

    merge.appendChild(
        blurNode
    );

    merge.appendChild(
        sourceNode
    );

    filter.appendChild(
        blur
    );

    filter.appendChild(
        merge
    );

    defs.appendChild(
        filter
    );

    svg.appendChild(
        defs
    );

    /*
     * ==========================================
     * BACKGROUND
     * ==========================================
     */

    const background =
        document.createElementNS(
            svgNS,
            "rect"
        );

    background.setAttribute(
        "x",
        "0"
    );

    background.setAttribute(
        "y",
        "0"
    );

    background.setAttribute(
        "width",
        "720"
    );

    background.setAttribute(
        "height",
        "720"
    );

    background.setAttribute(
        "rx",
        "20"
    );

    background.setAttribute(
        "fill",
        "url(#kundliCosmicGradient)"
    );

    svg.appendChild(
        background
    );

    /*
     * ==========================================
     * SUBTLE STARS
     * ==========================================
     */

    const stars = [
        [70, 75, 1.5],
        [125, 120, 1],
        [210, 70, 1.2],
        [305, 100, 1],
        [430, 75, 1.2],
        [535, 115, 1],
        [650, 75, 1.5],

        [70, 250, 1],
        [645, 250, 1.2],

        [75, 470, 1.1],
        [640, 470, 1],

        [100, 625, 1.3],
        [220, 655, 1],
        [370, 640, 1.2],
        [510, 655, 1],
        [640, 625, 1.3]
    ];

    stars.forEach(
        ([x, y, radius]) => {

            const star =
                document.createElementNS(
                    svgNS,
                    "circle"
                );

            star.setAttribute(
                "cx",
                x
            );

            star.setAttribute(
                "cy",
                y
            );

            star.setAttribute(
                "r",
                radius
            );

            star.setAttribute(
                "fill",
                "#7DD3FC"
            );

            star.setAttribute(
                "opacity",
                "0.7"
            );

            svg.appendChild(
                star
            );
        }
    );

    /*
     * ==========================================
     * OUTER SQUARE
     * ==========================================
     */

    const outer =
        document.createElementNS(
            svgNS,
            "rect"
        );

    outer.setAttribute(
        "x",
        "30"
    );

    outer.setAttribute(
        "y",
        "30"
    );

    outer.setAttribute(
        "width",
        "660"
    );

    outer.setAttribute(
        "height",
        "660"
    );

    outer.setAttribute(
        "fill",
        "none"
    );

    outer.setAttribute(
        "stroke",
        "#38BDF8"
    );

    outer.setAttribute(
        "stroke-width",
        "3"
    );

    outer.setAttribute(
        "rx",
        "2"
    );

    outer.setAttribute(
        "filter",
        "url(#kundliBlueGlow)"
    );

    svg.appendChild(
        outer
    );

    /*
     * ==========================================
     * NORTH INDIAN KUNDLI FORMATION
     *
     * This is the traditional fixed North
     * Indian diamond-house layout.
     * ==========================================
     */

    const chartLines = [

        /*
         * Diamond
         */

        [30, 360, 360, 30],

        [360, 30, 690, 360],

        [690, 360, 360, 690],

        [360, 690, 30, 360],

        /*
         * Four corner-to-center lines
         *
         * These create the 12 traditional
         * North Indian houses.
         */

        [30, 30, 360, 360],

        [690, 30, 360, 360],

        [30, 690, 360, 360],

        [690, 690, 360, 360]
    ];

    chartLines.forEach(
        ([x1, y1, x2, y2]) => {

            const line =
                document.createElementNS(
                    svgNS,
                    "line"
                );

            line.setAttribute(
                "x1",
                x1
            );

            line.setAttribute(
                "y1",
                y1
            );

            line.setAttribute(
                "x2",
                x2
            );

            line.setAttribute(
                "y2",
                y2
            );

            line.setAttribute(
                "stroke",
                "#38BDF8"
            );

            line.setAttribute(
                "stroke-width",
                "2.2"
            );

            line.setAttribute(
                "stroke-linecap",
                "round"
            );

            line.setAttribute(
                "opacity",
                "0.95"
            );

            svg.appendChild(
                line
            );
        }
    );

    /*
     * ==========================================
     * HOUSE CENTERS
     *
     * Fixed North Indian house positions.
     * ==========================================
     */

    const housePositions = {

        /*
         * 1st house
         * Top-center diamond
         */

        1: {
            x: 360,
            y: 170
        },

        /*
         * 2nd house
         * Top-left corner triangle
         */

        2: {
            x: 175,
            y: 105
        },

        /*
         * 3rd house
         * Left-upper diamond
         */

        3: {
            x: 115,
            y: 235
        },

        /*
         * 4th house
         * Left-center triangle
         */

        4: {
            x: 175,
            y: 360
        },

        /*
         * 5th house
         * Left-lower diamond
         */

        5: {
            x: 115,
            y: 485
        },

        /*
         * 6th house
         * Bottom-left corner
         */

        6: {
            x: 175,
            y: 615
        },

        /*
         * 7th house
         * Bottom-center
         */

        7: {
            x: 360,
            y: 550
        },

        /*
         * 8th house
         * Bottom-right corner
         */

        8: {
            x: 545,
            y: 615
        },

        /*
         * 9th house
         * Right-lower diamond
         */

        9: {
            x: 605,
            y: 485
        },

        /*
         * 10th house
         * Right-center
         */

        10: {
            x: 545,
            y: 360
        },

        /*
         * 11th house
         * Right-upper diamond
         */

        11: {
            x: 605,
            y: 235
        },

        /*
         * 12th house
         * Top-right corner
         */

        12: {
            x: 545,
            y: 105
        }
    };

    /*
     * ==========================================
     * PLANET ABBREVIATIONS
     * ==========================================
     */

    const fallbackSymbols = {

        Sun: "Sun",

        Moon: "Moon",

        Mars: "Mars",

        Mercury: "Merc",

        Jupiter: "Jup",

        Venus: "Ven",

        Saturn: "Sat",

        Rahu: "Rahu",

        Ketu: "Ketu"
    };

    /*
     * ==========================================
     * RENDER HOUSES
     * ==========================================
     */

    houses.forEach(
        (houseData) => {

            const position =
                housePositions[
                    houseData.house
                ];

            if (!position) {
                return;
            }

            const x =
                position.x;

            const y =
                position.y;

            /*
             * ----------------------------------
             * Zodiac sign number
             *
             * 1 = Aries
             * 2 = Taurus
             * ...
             * 12 = Pisces
             * ----------------------------------
             */

            if (
                houseData.sign !== null &&
                houseData.sign !== undefined
            ) {

                const signNumber =
                    Number(
                        houseData.sign
                    ) + 1;

                const signText =
                    document.createElementNS(
                        svgNS,
                        "text"
                    );

                signText.setAttribute(
                    "x",
                    x
                );

                signText.setAttribute(
                    "y",
                    y - 20
                );

                signText.setAttribute(
                    "text-anchor",
                    "middle"
                );

                signText.setAttribute(
                    "font-family",
                    "Arial, sans-serif"
                );

                signText.setAttribute(
                    "font-size",
                    "22"
                );

                signText.setAttribute(
                    "font-weight",
                    "600"
                );

                signText.setAttribute(
                    "fill",
                    "#7DD3FC"
                );

                signText.setAttribute(
                    "opacity",
                    "0.95"
                );

                signText.textContent =
                    String(
                        signNumber
                    );

                svg.appendChild(
                    signText
                );
            }

            /*
             * ----------------------------------
             * Planet positions
             * ----------------------------------
             */

            const planets =
                houseData.planets || [];

            const planetCount =
                planets.length;

            planets.forEach(
                (planet, index) => {

                    const name =
                        getPlanetName(
                            planet,
                            "Planet"
                        );

                    let symbol =
                        PLANET_SYMBOLS[
                            name
                        ];

                    if (
                        !symbol
                    ) {
                        symbol =
                            fallbackSymbols[
                                name
                            ];
                    }

                    if (
                        !symbol
                    ) {
                        symbol =
                            name
                                .substring(
                                    0,
                                    2
                                )
                                .toUpperCase();
                    }

                    /*
                     * --------------------------------
                     * Arrange multiple planets
                     * horizontally.
                     * --------------------------------
                     */

                    /*
                     * Keep planet labels separated and readable.
                     * The label uses a human-readable name (Sun, Moon, Merc,
                     * etc.) and the degree is shown directly underneath.
                     */
                    const columns = planetCount <= 2 ? planetCount : 2;
                    const rows = Math.ceil(planetCount / columns);
                    const columnSpacing = planetCount === 1 ? 0 : 54;
                    const rowSpacing = 38;
                    const column = index % columns;
                    const row = Math.floor(index / columns);

                    const px =
                        x +
                        (column - (columns - 1) / 2) *
                        columnSpacing;

                    const py =
                        y +
                        10 +
                        row * rowSpacing;

                    const planetText =
                        document.createElementNS(
                            svgNS,
                            "text"
                        );

                    planetText.setAttribute("x", px);
                    planetText.setAttribute("y", py);
                    planetText.setAttribute("text-anchor", "middle");
                    planetText.setAttribute("font-family", "Arial, sans-serif");
                    planetText.setAttribute("font-size", planetCount > 2 ? "17" : "19");
                    planetText.setAttribute("font-weight", "700");
                    planetText.setAttribute("fill", "#FFFFFF");
                    planetText.setAttribute("filter", "none");
                    planetText.textContent = symbol;

                    /* Native SVG tooltip: hover/tap the planet label for full details. */
                    const title = document.createElementNS(svgNS, "title");
                    const degree = getDegree(planet);
                    title.textContent =
                        `${name}${degree !== null ? ` — ${degree.toFixed(1)}°` : ""}`;
                    planetText.appendChild(title);

                    svg.appendChild(planetText);

                    if (degree !== null) {
                        const degreeText =
                            document.createElementNS(svgNS, "text");

                        degreeText.setAttribute("x", px);
                        degreeText.setAttribute("y", py + 18);
                        degreeText.setAttribute("text-anchor", "middle");
                        degreeText.setAttribute("font-family", "Arial, sans-serif");
                        degreeText.setAttribute("font-size", planetCount > 2 ? "12" : "13");
                        degreeText.setAttribute("font-weight", "600");
                        degreeText.setAttribute("fill", "#F3C96B");
                        degreeText.setAttribute("opacity", "0.95");
                        degreeText.textContent = `${degree.toFixed(1)}°`;
                        svg.appendChild(degreeText);
                    }
                }
            );
        }
    );

    /*
     * ==========================================
     * ASCENDANT MARKER
     * ==========================================
     */

    if (
    showAscendant &&
    ascSign !== null &&
    ascSign !== undefined
) {

        const ascendant =
            document.createElementNS(
                svgNS,
                "text"
            );

        ascendant.setAttribute(
            "x",
            "360"
        );

        ascendant.setAttribute(
            "y",
            "220"
        );

        ascendant.setAttribute(
            "text-anchor",
            "middle"
        );

        ascendant.setAttribute(
            "font-family",
            "Arial, sans-serif"
        );

        ascendant.setAttribute(
            "font-size",
            "24"
        );

        ascendant.setAttribute(
            "font-weight",
            "700"
        );

        ascendant.setAttribute(
            "fill",
            "#FFFFFF"
        );

        ascendant.textContent =
            "As";

        svg.appendChild(
            ascendant
        );
    }

    /*
     * ==========================================
     * CENTER GLOW
     * ==========================================
     */

    const center =
        document.createElementNS(
            svgNS,
            "circle"
        );

    center.setAttribute(
        "cx",
        "360"
    );

    center.setAttribute(
        "cy",
        "360"
    );

    center.setAttribute(
        "r",
        "3"
    );

    center.setAttribute(
        "fill",
        "#7DD3FC"
    );

    center.setAttribute(
        "filter",
        "url(#kundliBlueGlow)"
    );

    svg.appendChild(
        center
    );

    return svg;
}

    function renderNorthIndianChart(container, chart, options = {}) {
    const showAscendant = options.showAscendant !== false;
        if (!container) return;

        container.innerHTML = "";

        const wrapper =
            document.createElement(
                "div"
            );

        wrapper.className =
            "kundli-chart-visual";

        const svg =
            createNorthIndianSVG(
                chart,
                options
            );

        // Derived charts use the exact same visual treatment as the main Kundli.
        if (container.closest("#specialCharts")) {
            svg.classList.add("derived-kundli-svg");
        }

        wrapper.appendChild(svg);

        container.appendChild(
            wrapper
        );

        return svg;
    }

    /*
     * ------------------------------------------
     * Planet-position visual
     * ------------------------------------------
     *
     * This is generated from the actual calculated
     * longitude/sign data returned by the backend.
     */

    function createPlanetPositionVisual(
        chart
    ) {
        const wrapper =
            document.createElement(
                "div"
            );

        wrapper.className =
            "planet-position-visual";

        const header =
            document.createElement(
                "div"
            );

        header.className =
            "planet-position-header";

        header.innerHTML = `
            <div>
                <span class="section-eyebrow">
                    GRAHA PLACEMENTS
                </span>
                <h3>Planetary Positions</h3>
                <p>
                    Actual calculated planetary longitudes
                    across the zodiac.
                </p>
            </div>
        `;

        wrapper.appendChild(
            header
        );

        const wheel =
            document.createElement(
                "div"
            );

        wheel.className =
            "planet-zodiac-wheel";

        const zodiacRing =
            document.createElement(
                "div"
            );

        zodiacRing.className =
            "planet-zodiac-ring";

        ZODIAC_SIGNS.forEach(
            (sign, index) => {
                const segment =
                    document.createElement(
                        "div"
                    );

                segment.className =
                    "zodiac-segment";

                segment.dataset.sign =
                    index;

                segment.innerHTML = `
                    <span class="zodiac-symbol">
                        ${sign.symbol}
                    </span>
                    <span class="zodiac-name">
                        ${escapeHTML(sign.name)}
                    </span>
                `;

                zodiacRing.appendChild(
                    segment
                );
            }
        );

        wheel.appendChild(
            zodiacRing
        );

        const planetLayer =
            document.createElement(
                "div"
            );

        planetLayer.className =
            "planet-position-layer";

        const planets =
            getPlanets(chart);

        PLANET_NAMES.forEach(
            (planetName, index) => {
                const planet =
                    planets.find(
                        (item) =>
                            getPlanetName(
                                item
                            ).toLowerCase() ===
                            planetName.toLowerCase()
                    );

                if (!planet) return;

                const longitude =
                    getLongitude(
                        planet
                    );

                const signIndex =
                    getSignIndex(
                        planet
                    );

                if (
                    longitude === null &&
                    signIndex === null
                ) {
                    return;
                }

                let angle;

                if (
                    longitude !== null
                ) {
                    angle =
                        ((longitude % 360) +
                            360) %
                        360;
                } else {
                    angle =
                        signIndex * 30 +
                        number(
                            getDegree(
                                planet
                            )
                        );
                }

                /*
                 * SVG-like circular positioning.
                 * 0° is displayed at the top.
                 */
                const radians =
                    ((angle - 90) *
                        Math.PI) /
                    180;

                const radius =
                    37 +
                    (index % 3) * 5;

                const x =
                    50 +
                    radius *
                    Math.cos(
                        radians
                    );

                const y =
                    50 +
                    radius *
                    Math.sin(
                        radians
                    );

                const marker =
                    document.createElement(
                        "div"
                    );

                marker.className =
                    "planet-orbit-marker";

                marker.style.left =
                    `${x}%`;

                marker.style.top =
                    `${y}%`;

                const symbol =
                    PLANET_SYMBOLS[
                        planetName
                    ] || planetName.slice(
                        0,
                        2
                    );

                const degree =
                    getDegree(
                        planet
                    );

                const sign =
                    signIndex !== null
                        ? ZODIAC_SIGNS[
                            signIndex
                        ]
                        : null;

                marker.innerHTML = `
                    <span class="planet-marker-symbol">
                        ${escapeHTML(symbol)}
                    </span>
                    <span class="planet-marker-name">
                        ${escapeHTML(planetName)}
                    </span>
                    <span class="planet-marker-degree">
                        ${
                            degree === null
                                ? "—"
                                : `${degree.toFixed(2)}°`
                        }
                    </span>
                `;

                marker.title =
                    sign
                        ? `${planetName} — ${sign.name} ${degree === null ? "" : degree.toFixed(2) + "°"}`
                        : planetName;

                planetLayer.appendChild(
                    marker
                );
            }
        );

        wheel.appendChild(
            planetLayer
        );

        const center =
            document.createElement(
                "div"
            );

        center.className =
            "planet-wheel-center";

        center.innerHTML = `
            <span class="planet-wheel-center-symbol">
                ✦
            </span>
            <strong>RASHI</strong>
            <small>360° Zodiac</small>
        `;

        wheel.appendChild(
            center
        );

        wrapper.appendChild(
            wheel
        );

        /*
         * Compact legend/table.
         */
        const positionList =
            document.createElement(
                "div"
            );

        positionList.className =
            "planet-position-list";

        PLANET_NAMES.forEach(
            (planetName) => {
                const planet =
                    findPlanet(
                        chart,
                        planetName
                    );

                if (!planet) return;

                const signIndex =
                    getSignIndex(
                        planet
                    );

                const sign =
                    signIndex !== null
                        ? ZODIAC_SIGNS[
                            signIndex
                        ]
                        : null;

                const degree =
                    getDegree(
                        planet
                    );

                const house =
                    getHouse(
                        planet
                    );

                const item =
                    document.createElement(
                        "div"
                    );

                item.className =
                    "planet-position-item";

                item.innerHTML = `
                    <span class="planet-position-symbol">
                        ${escapeHTML(
                            PLANET_SYMBOLS[
                                planetName
                            ] ||
                            planetName.slice(
                                0,
                                2
                            )
                        )}
                    </span>

                    <span class="planet-position-name">
                        ${escapeHTML(
                            planetName
                        )}
                    </span>

                    <span class="planet-position-sign">
                        ${
                            sign
                                ? `${sign.symbol} ${escapeHTML(sign.name)}`
                                : "—"
                        }
                    </span>

                    <span class="planet-position-degree">
                        ${
                            degree === null
                                ? "—"
                                : `${degree.toFixed(2)}°`
                        }
                    </span>

                    <span class="planet-position-house">
                        ${
                            house
                                ? `House ${house}`
                                : "—"
                        }
                    </span>
                `;

                positionList.appendChild(
                    item
                );
            }
        );

        wrapper.appendChild(
            positionList
        );

        return wrapper;
    }

    function renderPlanetPositionVisual(
        container,
        chart
    ) {
        if (!container) return;

        container.innerHTML = "";

        const visual =
            createPlanetPositionVisual(
                chart
            );

        container.appendChild(
            visual
        );

        return visual;
    }

    /*
     * ------------------------------------------
     * Chandra Kundli + Navamsha D9
     * ------------------------------------------
     */

    function getAbsoluteLongitude(body) {
        const longitude = getLongitude(body);

        if (longitude !== null) {
            return ((longitude % 360) + 360) % 360;
        }

        const sign = getSignIndex(body);
        const degree = getDegree(body);

        if (sign === null || degree === null) {
            return null;
        }

        return sign * 30 + degree;
    }

    function getNavamshaSign(longitude) {
        if (longitude === null) return null;

        const normalized = ((longitude % 360) + 360) % 360;
        const rashi = Math.floor(normalized / 30);
        const degreeInSign = normalized % 30;
        const navamsaIndex = Math.min(8, Math.floor(degreeInSign / (30 / 9)));

        // Movable: Aries, Cancer, Libra, Capricorn.
        const movable = [0, 3, 6, 9];
        // Fixed: Taurus, Leo, Scorpio, Aquarius.
        const fixed = [1, 4, 7, 10];

        let startingSign;

        if (movable.includes(rashi)) {
            startingSign = rashi;
        } else if (fixed.includes(rashi)) {
            startingSign = (rashi + 8) % 12;
        } else {
            // Dual: Gemini, Virgo, Sagittarius, Pisces.
            startingSign = (rashi + 4) % 12;
        }

        return (startingSign + navamsaIndex) % 12;
    }

    function createDerivedPlanet(planet, signIndex, house) {
        return {
            ...planet,
            sign_index: signIndex,
            signIndex: signIndex,
            house: house,
            degree: getDegree(planet) ?? 0
        };
    }

    function createChandraChart(chart) {
        if (!chart) return null;

        const moon = findPlanet(chart, "Moon");
        if (!moon) return null;

        const moonSign = getSignIndex(moon);
        if (moonSign === null) return null;

        const chandraPlanets = getPlanets(chart).map(planet => {
            const sign = getSignIndex(planet);
            if (sign === null) return planet;

            const house = ((sign - moonSign + 12) % 12) + 1;
            return createDerivedPlanet(planet, sign, house);
        });

        return {
            ...chart,
            ascendant: {
                sign_index: moonSign,
                signIndex: moonSign,
                name: "Moon"
            },
            asc: {
                sign_index: moonSign,
                signIndex: moonSign,
                name: "Moon"
            },
            planets: chandraPlanets
        };
    }

    function createNavamshaChart(chart) {
        if (!chart) return null;

        const ascendant = getAscendant(chart);
        if (!ascendant) return null;

        const ascLongitude = getAbsoluteLongitude(ascendant);
        if (ascLongitude === null) return null;

        const navamshaAsc = getNavamshaSign(ascLongitude);
        if (navamshaAsc === null) return null;

        const navamshaPlanets = getPlanets(chart).map(planet => {
            const longitude = getAbsoluteLongitude(planet);
            if (longitude === null) return planet;

            const d9Sign = getNavamshaSign(longitude);
            if (d9Sign === null) return planet;

            const house = ((d9Sign - navamshaAsc + 12) % 12) + 1;
            return createDerivedPlanet(planet, d9Sign, house);
        });

        return {
            ...chart,
            ascendant: {
                sign_index: navamshaAsc,
                signIndex: navamshaAsc,
                name: "Ascendant"
            },
            asc: {
                sign_index: navamshaAsc,
                signIndex: navamshaAsc,
                name: "Ascendant"
            },
            planets: navamshaPlanets
        };
    }

    function renderSpecialCharts(chart) {
        const chandraContainer = document.getElementById("chandraChart");
        const navamshaContainer = document.getElementById("navamshaChart");

        if (!chandraContainer && !navamshaContainer) return;

        if (chandraContainer) {
            const chandraChart = createChandraChart(chart);
            chandraContainer.innerHTML = "";

            if (chandraChart) {
                renderNorthIndianChart(chandraContainer, chandraChart, {showAscendant: false});
            } else {
                chandraContainer.innerHTML = '<div class="chart-empty">Chandra Kundli unavailable.</div>';
            }
        }

        if (navamshaContainer) {
            const navamshaChart = createNavamshaChart(chart);
            navamshaContainer.innerHTML = "";

            if (navamshaChart) {
                renderNorthIndianChart(navamshaContainer, navamshaChart, {showAscendant: false});
            } else {
                navamshaContainer.innerHTML = '<div class="chart-empty">Navamsha D9 unavailable.</div>';
            }
        }
    }

    /*
     * ------------------------------------------
     * Generic chart helper
     * ------------------------------------------
     */

    function renderChart(
        container,
        chart,
        type = "north-indian"
    ) {
        if (!container) return;

        if (
            type === "planet-position" ||
            type === "planetary"
        ) {
            return renderPlanetPositionVisual(
                container,
                chart
            );
        }

        return renderNorthIndianChart(
            container,
            chart
        );
    }

    /*
     * Public module.
     */
    window.AIJyotishCharts = {
        zodiacSigns: ZODIAC_SIGNS,
        planetSymbols: PLANET_SYMBOLS,

        getPlanets,
        getSignIndex,
        getHouse,
        getDegree,
        getLongitude,
        getAscendant,
        getAscendantSign,

        createNorthIndianSVG,
        renderNorthIndianChart,

        createPlanetPositionVisual,
        renderPlanetPositionVisual,

        createChandraChart,
        createNavamshaChart,
        renderSpecialCharts,

        renderChart
    };

    /*
     * Backward-compatible global aliases.
     */
    window.renderNorthIndianChart =
        renderNorthIndianChart;

    window.renderPlanetPositionVisual =
        renderPlanetPositionVisual;

    window.renderSpecialCharts =
        renderSpecialCharts;
})();