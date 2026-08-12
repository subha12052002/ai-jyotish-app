/* =========================================================
   AI JYOTISH - MAIN JAVASCRIPT
   North Indian Kundli
   Flask + Gemini AI
========================================================= */


/* =========================================================
   API
========================================================= */

const API_URL = "/api/kundli";
const AI_API_URL = "/api/ai";


/* =========================================================
   SIGNS
========================================================= */

const SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
];


/* =========================================================
   PLANETS
========================================================= */

const PLANET_NAMES = {
    Sun: "Su",
    Moon: "Mo",
    Mars: "Ma",
    Mercury: "Me",
    Jupiter: "Ju",
    Venus: "Ve",
    Saturn: "Sa",
    Rahu: "Ra",
    Ketu: "Ke"
};


/* =========================================================
   NAKSHATRAS
========================================================= */

const NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati"
];


/* =========================================================
   HELPERS
========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


function safeNumber(value, fallback = null) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return fallback;
    }

    const number = Number(value);

    return Number.isFinite(number)
        ? number
        : fallback;
}


/* =========================================================
   SIGN NORMALIZATION
========================================================= */

function normalizeSign(value, zeroBased = false) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return null;
    }

    if (typeof value === "number") {

        if (zeroBased) {

            if (
                Number.isInteger(value) &&
                value >= 0 &&
                value <= 11
            ) {
                return value;
            }

        } else {

            if (
                Number.isInteger(value) &&
                value >= 1 &&
                value <= 12
            ) {
                return value - 1;
            }
        }
    }

    const text = String(value).trim();

    const lower = text.toLowerCase();

    const index = SIGNS.findIndex(
        sign =>
            sign.toLowerCase() === lower
    );

    if (index !== -1) {
        return index;
    }

    const match = text.match(/\d+/);

    if (match) {

        const number = Number(match[0]);

        if (
            number >= 1 &&
            number <= 12
        ) {
            return number - 1;
        }
    }

    return null;
}


function signName(index) {

    if (
        index === null ||
        index === undefined ||
        index < 0 ||
        index > 11
    ) {
        return "—";
    }

    return SIGNS[index];
}


/* =========================================================
   DEGREE
========================================================= */

function formatDegree(value) {

    const number = safeNumber(value);

    if (number === null) {
        return "—";
    }

    return `${number.toFixed(2)}°`;
}


function degreeToDMS(value) {

    const number = safeNumber(value);

    if (number === null) {
        return "—";
    }

    let degrees = Math.floor(number);

    let minutesDecimal =
        (number - degrees) * 60;

    let minutes =
        Math.floor(minutesDecimal);

    let seconds =
        Math.round(
            (minutesDecimal - minutes) * 60
        );

    if (seconds === 60) {
        seconds = 0;
        minutes++;
    }

    if (minutes === 60) {
        minutes = 0;
        degrees++;
    }

    return `${degrees}° ${minutes}' ${seconds}"`;
}


/* =========================================================
   NAKSHATRA
========================================================= */

function calculateNakshatra(longitude) {

    if (longitude === null) {
        return "—";
    }

    const normalized =
        ((longitude % 360) + 360) % 360;

    const size = 360 / 27;

    const index =
        Math.floor(
            normalized / size
        );

    return NAKSHATRAS[index] || "—";
}


/* =========================================================
   PLANET NORMALIZATION
========================================================= */

function normalizePlanets(result) {

    const source = result?.planets;

    if (!source) {
        return [];
    }

    const planets = [];

    if (Array.isArray(source)) {

        source.forEach(
            (planet, index) => {

                if (!planet) {
                    return;
                }

                planets.push(
                    normalizePlanet(
                        planet,
                        index
                    )
                );
            }
        );

    } else {

        Object.entries(source)
            .forEach(
                ([name, value], index) => {

                    let planet;

                    if (
                        value &&
                        typeof value === "object" &&
                        !Array.isArray(value)
                    ) {

                        planet = {
                            ...value,
                            name:
                                value.name ||
                                value.planet ||
                                name
                        };

                    } else {

                        planet = {
                            name,
                            longitude: value
                        };
                    }

                    planets.push(
                        normalizePlanet(
                            planet,
                            index
                        )
                    );
                }
            );
    }

    return planets.filter(
        planet =>
            planet &&
            planet.name
    );
}


/* =========================================================
   NORMALIZE ONE PLANET
========================================================= */

function normalizePlanet(
    planet,
    index
) {

    const name =
        planet.name ||
        planet.planet ||
        planet.body ||
        `Planet ${index + 1}`;

    let longitude =
        planet.longitude ??
        planet.lon ??
        planet.longitude_degree ??
        planet.absolute_longitude ??
        null;

    longitude = safeNumber(longitude);

    let sign =
        planet.sign ??
        planet.rashi ??
        planet.zodiac ??
        planet.sign_name ??
        null;

    let signIndex = null;

    if (longitude !== null) {

        const normalizedLongitude =
            ((longitude % 360) + 360) % 360;

        signIndex =
            Math.floor(
                normalizedLongitude / 30
            );
    }

    if (signIndex === null) {

        signIndex =
            normalizeSign(
                sign,
                false
            );
    }

    let degreeInSign =
        planet.degree_in_sign ??
        planet.sign_degree ??
        planet.degrees ??
        null;

    degreeInSign =
        safeNumber(
            degreeInSign
        );

    if (
        degreeInSign === null &&
        longitude !== null
    ) {

        const normalizedLongitude =
            ((longitude % 360) + 360) % 360;

        degreeInSign =
            normalizedLongitude % 30;
    }

    const nakshatra =
        planet.nakshatra ||
        planet.nakshatra_name ||
        calculateNakshatra(
            longitude
        );

    const house =
        safeNumber(
            planet.house ??
            planet.house_number
        );

    const retrograde =
        planet.retrograde ??
        planet.is_retrograde ??
        false;

    return {

        name,

        short:
            PLANET_NAMES[name] ||
            name.substring(0, 2),

        longitude,

        signIndex,

        sign:
            signIndex !== null
                ? SIGNS[signIndex]
                : sign || "—",

        degree:
            degreeInSign,

        nakshatra,

        house,

        retrograde:
            Boolean(retrograde)
    };
}


/* =========================================================
   ASCENDANT
========================================================= */

function getAscendantIndex(result) {

    const asc = result?.ascendant;

    if (
        asc &&
        typeof asc === "object"
    ) {

        const longitude =
            safeNumber(
                asc.longitude ??
                asc.lon ??
                asc.longitude_degree
            );

        if (longitude !== null) {

            return Math.floor(
                (
                    ((longitude % 360) + 360) % 360
                ) / 30
            );
        }

        return normalizeSign(
            asc.sign ??
            asc.rashi ??
            asc.zodiac ??
            asc.name,
            false
        );
    }

    return normalizeSign(
        asc,
        false
    );
}


function getAscendantDegree(result) {

    const asc = result?.ascendant;

    if (!asc) {
        return null;
    }

    if (
        typeof asc === "object"
    ) {

        let degree =
            asc.degree_in_sign ??
            asc.sign_degree ??
            asc.degrees ??
            null;

        degree = safeNumber(degree);

        if (degree !== null) {
            return degree;
        }

        const longitude =
            safeNumber(
                asc.longitude ??
                asc.lon ??
                asc.longitude_degree
            );

        if (longitude !== null) {

            const normalized =
                ((longitude % 360) + 360) % 360;

            return normalized % 30;
        }
    }

    return null;
}


/* =========================================================
   BIRTH FORM
========================================================= */

function initializeBirthForm() {

    const form = getElement("birthForm");

    if (!form) {
        return;
    }

    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const errorBox =
                getElement("formError");

            if (errorBox) {
                errorBox.textContent = "";
            }

            const button =
                getElement(
                    "createKundliButton"
                );

            const buttonText =
                getElement(
                    "buttonText"
                );

            const loader =
                getElement(
                    "buttonLoader"
                );

            if (button) {
                button.disabled = true;
            }

            if (buttonText) {
                buttonText.classList.add(
                    "hidden"
                );
            }

            if (loader) {
                loader.classList.remove(
                    "hidden"
                );
            }

            const data = {

                name:
                    getElement("name")?.value.trim(),

                date:
                    getElement("date")?.value,

                time:
                    getElement("time")?.value,

                place:
                    getElement("place")?.value.trim(),

                latitude:
                    getElement("latitude")?.value,

                longitude:
                    getElement("longitude")?.value,

                timezone:
                    getElement("timezone")?.value
            };

            console.log(
                "Sending Kundli data:",
                data
            );

            try {

                const response =
                    await fetch(
                        API_URL,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)
                        }
                    );

                const result =
                    await response.json();

                console.log(
                    "Kundli API response:",
                    result
                );

                if (!response.ok) {

                    throw new Error(
                        result.error ||
                        result.details ||
                        "Kundli calculation failed."
                    );
                }

                if (
                    result.success !== true
                ) {

                    throw new Error(
                        result.error ||
                        "Kundli was not created."
                    );
                }

                sessionStorage.setItem(
                    "kundliData",
                    JSON.stringify(result)
                );

                window.location.href =
                    "kundli.html";

            } catch (error) {

                console.error(
                    "Kundli error:",
                    error
                );

                if (errorBox) {

                    errorBox.textContent =
                        error.message ||
                        "Unable to create Kundli.";
                }

            } finally {

                if (button) {
                    button.disabled = false;
                }

                if (buttonText) {
                    buttonText.classList.remove(
                        "hidden"
                    );
                }

                if (loader) {
                    loader.classList.add(
                        "hidden"
                    );
                }
            }
        }
    );
}


/* =========================================================
   KUNDLI PAGE
========================================================= */

function initializeKundliPage() {

    const lagnaChart =
        getElement("lagnaChart");

    if (!lagnaChart) {
        return;
    }

    const raw =
        sessionStorage.getItem(
            "kundliData"
        );

    if (!raw) {

        showKundliError(
            "No Kundli data found. Please create a new Kundli."
        );

        return;
    }

    let result;

    try {

        result =
            JSON.parse(raw);

    } catch (error) {

        showKundliError(
            "Saved Kundli data is invalid."
        );

        return;
    }

    console.log(
        "========== KUNDLI RESULT =========="
    );

    console.log(result);

    const planets =
        normalizePlanets(result);

    console.table(planets);

    renderProfile(result);

    renderQuickDetails(
        result,
        planets
    );

    renderLagnaChart(
        result,
        planets
    );

    renderChandraChart(
        result,
        planets
    );

    renderPlanetTable(
        planets
    );

    renderYuti(
        planets
    );

    renderStrength(
        planets
    );

    renderHouses(
        result,
        planets
    );

    renderAspects(
        planets
    );

    renderNakshatra(
        planets
    );

    renderYogas(
        result,
        planets
    );

    initializeAIForm(
        result,
        planets
    );
}


/* =========================================================
   PROFILE
========================================================= */

function renderProfile(result) {

    const name =
        result.name ||
        "Your Kundli";

    const date =
        result.birth_date ||
        result.date ||
        "—";

    const time =
        result.birth_time ||
        result.time ||
        "—";

    const place =
        result.birth_place ||
        result.place ||
        "—";

    const personName =
        getElement("personName");

    if (personName) {
        personName.textContent = name;
    }

    const personInfo =
        getElement("personInfo");

    if (personInfo) {

        personInfo.textContent =
            `${date} • ${time} • ${place}`;
    }

    const ascIndex =
        getAscendantIndex(result);

    const ascendantSign =
        getElement("ascendantSign");

    if (ascendantSign) {

        ascendantSign.textContent =
            signName(ascIndex);
    }

    const lagnaChartSign =
        getElement("lagnaChartSign");

    if (lagnaChartSign) {

        lagnaChartSign.textContent =
            signName(ascIndex);
    }
}


/* =========================================================
   QUICK DETAILS
========================================================= */

function renderQuickDetails(
    result,
    planets
) {

    const ascIndex =
        getAscendantIndex(result);

    const ascDegree =
        getAscendantDegree(result);

    const ascendantValue =
        getElement("ascendantValue");

    if (ascendantValue) {

        ascendantValue.textContent =
            signName(ascIndex);
    }

    const ascendantDegree =
        getElement("ascendantDegree");

    if (ascendantDegree) {

        ascendantDegree.textContent =
            ascDegree === null
                ? "—"
                : degreeToDMS(
                    ascDegree
                );
    }

    const sun =
        findPlanet(
            planets,
            "Sun"
        );

    const moon =
        findPlanet(
            planets,
            "Moon"
        );

    const sunSign =
        getElement("sunSign");

    if (sunSign) {

        sunSign.textContent =
            sun
                ? sun.sign
                : "—";
    }

    const moonSign =
        getElement("moonSign");

    if (moonSign) {

        moonSign.textContent =
            moon
                ? moon.sign
                : "—";
    }

    const moonDegree =
        getElement("moonDegree");

    if (moonDegree) {

        moonDegree.textContent =
            moon
                ? formatDegree(
                    moon.degree
                )
                : "—";
    }

    const moonNakshatra =
        getElement("moonNakshatra");

    if (moonNakshatra) {

        moonNakshatra.textContent =
            moon
                ? moon.nakshatra
                : "—";
    }

    const chandraChartSign =
        getElement("chandraChartSign");

    if (chandraChartSign) {

        chandraChartSign.textContent =
            moon
                ? moon.sign
                : "—";
    }
}


/* =========================================================
   FIND PLANET
========================================================= */

function findPlanet(
    planets,
    name
) {

    return planets.find(
        planet =>
            planet.name &&
            planet.name.toLowerCase() ===
            name.toLowerCase()
    );
}


/* =========================================================
   NORTH INDIAN CHART
========================================================= */

function createNorthIndianChart(
    planets,
    startingSign,
    ascendantSign,
    chartType
) {

    if (
        startingSign === null ||
        startingSign === undefined
    ) {

        return `
            <div class="muted">
                Chart data unavailable.
            </div>
        `;
    }

    const positions = [

        { x: 250, y: 130 },
        { x: 135, y: 80 },
        { x: 75, y: 145 },
        { x: 75, y: 250 },
        { x: 75, y: 355 },
        { x: 135, y: 420 },
        { x: 250, y: 370 },
        { x: 365, y: 420 },
        { x: 425, y: 355 },
        { x: 425, y: 250 },
        { x: 425, y: 145 },
        { x: 365, y: 80 }

    ];

    const housePlanets =
        Array.from(
            { length: 12 },
            () => []
        );

    planets.forEach(
        planet => {

            if (
                planet.signIndex === null
            ) {
                return;
            }

            const house =
                (
                    planet.signIndex -
                    startingSign +
                    12
                ) % 12;

            housePlanets[
                house
            ].push(
                planet
            );
        }
    );

    let signText = "";

    for (
        let house = 0;
        house < 12;
        house++
    ) {

        const signIndex =
            (
                startingSign +
                house
            ) % 12;

        const pos =
            positions[house];

        signText += `

            <text
                x="${pos.x}"
                y="${pos.y - 35}"
                class="chart-house-number"
                text-anchor="middle"
            >
                ${signIndex + 1}
            </text>
        `;
    }

    let planetText = "";

    housePlanets.forEach(
        (items, houseIndex) => {

            if (!items.length) {
                return;
            }

            const pos =
                positions[houseIndex];

            let displayItems =
                [...items];

            if (
                chartType === "lagna" &&
                houseIndex === 0 &&
                ascendantSign === startingSign
            ) {

                displayItems.unshift({
                    short: "Asc"
                });
            }

            const lineHeight =
                displayItems.length > 4
                    ? 19
                    : 23;

            const totalHeight =
                displayItems.length *
                lineHeight;

            const startY =
                pos.y -
                (totalHeight / 2) +
                5;

            displayItems.forEach(
                (planet, index) => {

                    const y =
                        startY +
                        (
                            index *
                            lineHeight
                        );

                    const isAsc =
                        planet.short === "Asc";

                    planetText += `

                        <text
                            x="${pos.x}"
                            y="${y}"
                            text-anchor="middle"
                            class="${
                                isAsc
                                    ? "chart-asc"
                                    : "chart-planet"
                            }"
                        >
                            ${escapeHTML(
                                planet.short
                            )}
                        </text>
                    `;
                }
            );
        }
    );

    return `

        <svg
            viewBox="0 0 500 500"
            class="kundli-svg"
            xmlns="http://www.w3.org/2000/svg"
        >

            <rect
                x="5"
                y="5"
                width="490"
                height="490"
                class="chart-border"
            />

            <line
                x1="5"
                y1="5"
                x2="495"
                y2="495"
                class="chart-line"
            />

            <line
                x1="495"
                y1="5"
                x2="5"
                y2="495"
                class="chart-line"
            />

            <polygon
                points="
                    250,5
                    495,250
                    250,495
                    5,250
                "
                class="chart-line"
            />

            <polygon
                points="
                    250,155
                    345,250
                    250,345
                    155,250
                "
                class="chart-line"
            />

            ${signText}

            ${planetText}

        </svg>
    `;
}


/* =========================================================
   LAGNA CHART
========================================================= */

function renderLagnaChart(
    result,
    planets
) {

    const container =
        getElement(
            "lagnaChart"
        );

    if (!container) {
        return;
    }

    const ascIndex =
        getAscendantIndex(result);

    if (ascIndex === null) {

        container.innerHTML = `
            <div class="muted">
                Ascendant data unavailable.
            </div>
        `;

        return;
    }

    container.innerHTML =
        createNorthIndianChart(
            planets,
            ascIndex,
            ascIndex,
            "lagna"
        );
}


/* =========================================================
   CHANDRA CHART
========================================================= */

function renderChandraChart(
    result,
    planets
) {

    const container =
        getElement(
            "chandraChart"
        );

    if (!container) {
        return;
    }

    const moon =
        findPlanet(
            planets,
            "Moon"
        );

    if (
        !moon ||
        moon.signIndex === null
    ) {

        container.innerHTML = `
            <div class="muted">
                Moon data unavailable.
            </div>
        `;

        return;
    }

    container.innerHTML =
        createNorthIndianChart(
            planets,
            moon.signIndex,
            null,
            "chandra"
        );
}


/* =========================================================
   PLANET TABLE
========================================================= */

function renderPlanetTable(
    planets
) {

    const tbody =
        getElement(
            "planetTable"
        );

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    if (!planets.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    No planetary data available.
                </td>
            </tr>
        `;

        return;
    }

    planets.forEach(
        planet => {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `

                <td>
                    <strong>
                        ${escapeHTML(
                            planet.name
                        )}
                    </strong>
                </td>

                <td>
                    ${escapeHTML(
                        planet.sign
                    )}
                </td>

                <td>
                    ${
                        planet.degree === null
                            ? "—"
                            : degreeToDMS(
                                planet.degree
                            )
                    }
                </td>

                <td>
                    ${escapeHTML(
                        planet.nakshatra
                    )}
                </td>

                <td>
                    ${
                        planet.house === null
                            ? "—"
                            : planet.house
                    }
                </td>

                <td>
                    ${
                        planet.retrograde
                            ? "Retrograde"
                            : "Direct"
                    }
                </td>
            `;

            tbody.appendChild(row);
        }
    );
}


/* =========================================================
   GRAHA YUTI
========================================================= */

function renderYuti(
    planets
) {

    const container =
        getElement(
            "yutiContent"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const groups = {};

    planets.forEach(
        planet => {

            if (
                planet.signIndex === null
            ) {
                return;
            }

            const key =
                planet.signIndex;

            if (!groups[key]) {
                groups[key] = [];
            }

            groups[key].push(
                planet
            );
        }
    );

    const conjunctions =
        Object.values(groups)
            .filter(
                group =>
                    group.length >= 2
            );

    if (!conjunctions.length) {

        container.innerHTML = `
            <div class="yoga-card">

                <h3>
                    No major Graha Yuti
                </h3>

                <p class="muted">
                    No two or more planets are
                    placed in the same zodiac sign.
                </p>

            </div>
        `;

        return;
    }

    conjunctions.forEach(
        group => {

            const names =
                group
                    .map(
                        planet =>
                            planet.name
                    )
                    .join(" + ");

            const sign =
                group[0].sign;

            const degrees =
                group
                    .map(
                        planet =>
                            `${planet.name} ${formatDegree(
                                planet.degree
                            )}`
                    )
                    .join(" • ");

            container.innerHTML += `
                <div class="yoga-card">

                    <p class="eyebrow">
                        GRAHA YUTI
                    </p>

                    <h3>
                        ${escapeHTML(
                            names
                        )}
                    </h3>

                    <p>
                        ${escapeHTML(
                            sign
                        )}
                    </p>

                    <p class="muted">
                        ${escapeHTML(
                            degrees
                        )}
                    </p>

                </div>
            `;
        }
    );
}


/* =========================================================
   PLANETARY STRENGTH
========================================================= */

function renderStrength(
    planets
) {

    const container =
        getElement(
            "strengthContent"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    planets.forEach(
        planet => {

            let score = 50;

            let condition =
                "Neutral";

            const sign =
                planet.sign;

            if (
                planet.name === "Sun" &&
                sign === "Aries"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Sun" &&
                sign === "Libra"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Moon" &&
                sign === "Taurus"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Moon" &&
                sign === "Scorpio"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Mars" &&
                sign === "Capricorn"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Mars" &&
                sign === "Cancer"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Mercury" &&
                sign === "Virgo"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Mercury" &&
                sign === "Pisces"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Jupiter" &&
                sign === "Cancer"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Jupiter" &&
                sign === "Capricorn"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Venus" &&
                sign === "Pisces"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Venus" &&
                sign === "Virgo"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            else if (
                planet.name === "Saturn" &&
                sign === "Libra"
            ) {

                score = 90;
                condition = "Exalted";

            }

            else if (
                planet.name === "Saturn" &&
                sign === "Aries"
            ) {

                score = 20;
                condition = "Debilitated";
            }

            container.innerHTML += `
                <div class="strength-card">

                    <h3>
                        ${escapeHTML(
                            planet.name
                        )}
                    </h3>

                    <p class="muted">
                        ${escapeHTML(
                            condition
                        )}
                    </p>

                    <div class="strength-bar">

                        <div
                            class="strength-fill"
                            style="width:${score}%"
                        ></div>

                    </div>

                </div>
            `;
        }
    );
}


/* =========================================================
   HOUSES
========================================================= */

function renderHouses(
    result,
    planets
) {

    const container =
        getElement(
            "houseCards"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const houseGroups =
        Array.from(
            { length: 12 },
            () => []
        );

    planets.forEach(
        planet => {

            if (
                planet.house !== null &&
                planet.house >= 1 &&
                planet.house <= 12
            ) {

                houseGroups[
                    planet.house - 1
                ].push(
                    planet.name
                );
            }
        }
    );

    for (
        let i = 0;
        i < 12;
        i++
    ) {

        const content =
            houseGroups[i].length
                ? houseGroups[i].join(", ")
                : "No planets";

        container.innerHTML += `
            <div class="house-card">

                <p class="eyebrow">
                    HOUSE ${i + 1}
                </p>

                <h3>
                    ${houseMeaning(
                        i + 1
                    )}
                </h3>

                <p class="muted">
                    ${escapeHTML(
                        content
                    )}
                </p>

            </div>
        `;
    }
}


/* =========================================================
   HOUSE MEANINGS
========================================================= */

function houseMeaning(house) {

    const meanings = {

        1: "Self & Personality",
        2: "Wealth & Family",
        3: "Courage & Siblings",
        4: "Home & Mother",
        5: "Education & Creativity",
        6: "Health & Service",
        7: "Marriage & Partnership",
        8: "Transformation",
        9: "Dharma & Fortune",
        10: "Career & Status",
        11: "Gains & Networks",
        12: "Expenses & Spirituality"

    };

    return meanings[house] ||
        `House ${house}`;
}


/* =========================================================
   ASPECTS
========================================================= */

function renderAspects(planets) {

    const container =
        getElement(
            "aspectContent"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    planets.forEach(
        planet => {

            if (
                planet.signIndex === null
            ) {
                return;
            }

            let aspects = [7];

            if (
                planet.name === "Mars"
            ) {

                aspects = [
                    4,
                    7,
                    8
                ];

            }

            else if (
                planet.name === "Jupiter"
            ) {

                aspects = [
                    5,
                    7,
                    9
                ];

            }

            else if (
                planet.name === "Saturn"
            ) {

                aspects = [
                    3,
                    7,
                    10
                ];
            }

            const targetSigns =
                aspects.map(
                    aspect => {

                        const index =
                            (
                                planet.signIndex +
                                aspect -
                                1
                            ) % 12;

                        return SIGNS[index];
                    }
                );

            container.innerHTML += `
                <div class="aspect-card">

                    <p class="eyebrow">
                        DRISHTI
                    </p>

                    <h3>
                        ${escapeHTML(
                            planet.name
                        )}
                    </h3>

                    <p class="muted">
                        Aspects:
                        ${escapeHTML(
                            targetSigns.join(", ")
                        )}
                    </p>

                </div>
            `;
        }
    );
}


/* =========================================================
   NAKSHATRA
========================================================= */

function renderNakshatra(planets) {

    const container =
        getElement(
            "nakshatraContent"
        );

    if (!container) {
        return;
    }

    const moon =
        findPlanet(
            planets,
            "Moon"
        );

    if (!moon) {

        container.innerHTML = `
            <p class="muted">
                Moon data unavailable.
            </p>
        `;

        return;
    }

    let pada = "—";

    if (
        moon.longitude !== null
    ) {

        const normalized =
            (
                moon.longitude %
                360 +
                360
            ) % 360;

        const nakshatraSize =
            360 / 27;

        const padaSize =
            nakshatraSize / 4;

        pada =
            Math.floor(
                (
                    normalized %
                    nakshatraSize
                ) / padaSize
            ) + 1;
    }

    container.innerHTML = `

        <div class="nakshatra-item">

            <span>
                Nakshatra
            </span>

            <strong>
                ${escapeHTML(
                    moon.nakshatra
                )}
            </strong>

        </div>

        <div class="nakshatra-item">

            <span>
                Moon Sign
            </span>

            <strong>
                ${escapeHTML(
                    moon.sign
                )}
            </strong>

        </div>

        <div class="nakshatra-item">

            <span>
                Degree
            </span>

            <strong>
                ${degreeToDMS(
                    moon.degree
                )}
            </strong>

        </div>

        <div class="nakshatra-item">

            <span>
                Pada
            </span>

            <strong>
                ${pada}
            </strong>

        </div>
    `;
}


/* =========================================================
   YOGAS
========================================================= */

function renderYogas(
    result,
    planets
) {

    const container =
        getElement(
            "yogaContent"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const sun =
        findPlanet(
            planets,
            "Sun"
        );

    const moon =
        findPlanet(
            planets,
            "Moon"
        );

    const mars =
        findPlanet(
            planets,
            "Mars"
        );

    const jupiter =
        findPlanet(
            planets,
            "Jupiter"
        );

    let found = false;

    if (
        sun &&
        moon &&
        sun.signIndex ===
        moon.signIndex
    ) {

        addYoga(
            container,
            "Sun-Moon Yuti",
            "Sun and Moon are placed in the same sign."
        );

        found = true;
    }

    if (
        mars &&
        jupiter &&
        mars.signIndex ===
        jupiter.signIndex
    ) {

        addYoga(
            container,
            "Mars-Jupiter Yuti",
            "Mars and Jupiter occupy the same zodiac sign."
        );

        found = true;
    }

    if (
        planets.length >= 7
    ) {

        addYoga(
            container,
            "Strong Planetary Activity",
            "Multiple classical planets are available for detailed chart analysis."
        );

        found = true;
    }

    if (!found) {

        addYoga(
            container,
            "No Basic Yoga Detected",
            "No basic combination was detected from the available API data."
        );
    }
}


/* =========================================================
   ADD YOGA
========================================================= */

function addYoga(
    container,
    title,
    description
) {

    container.innerHTML += `

        <div class="yoga-card">

            <p class="eyebrow">
                YOGA
            </p>

            <h3>
                ${escapeHTML(
                    title
                )}
            </h3>

            <p class="muted">
                ${escapeHTML(
                    description
                )}
            </p>

        </div>
    `;
}


/* =========================================================
   AI FORM
   FIXED VERSION
========================================================= */

function initializeAIForm(
    result,
    planets
) {

    const form =
        getElement("aiForm");

    if (!form) {
        console.log(
            "AI form not found."
        );
        return;
    }

    /*
       Prevent duplicate event listeners
       if this function is accidentally called again.
    */

    if (
        form.dataset.aiInitialized === "true"
    ) {
        return;
    }

    form.dataset.aiInitialized = "true";


    form.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const input =
                getElement(
                    "aiQuestion"
                );

            const messages =
                getElement(
                    "aiMessages"
                );


            if (
                !input ||
                !messages
            ) {

                console.error(
                    "AI input or messages container not found."
                );

                return;
            }


            const question =
                input.value.trim();


            if (!question) {
                return;
            }


            /* ============================================
               SHOW USER MESSAGE
            ============================================ */

            messages.innerHTML += `

                <div class="ai-message">

                    <strong>
                        You
                    </strong>

                    <p>
                        ${escapeHTML(
                            question
                        )}
                    </p>

                </div>
            `;


            input.value = "";


            /* ============================================
               LOADING
            ============================================ */

            const loadingId =
                "ai-loading-" +
                Date.now();


            messages.innerHTML += `

                <div
                    class="ai-message"
                    id="${loadingId}"
                >

                    <strong>
                        AI Jyotish
                    </strong>

                    <p>
                        Thinking...
                    </p>

                </div>
            `;


            const loading =
                getElement(
                    loadingId
                );


            /* ============================================
               DISABLE BUTTON
            ============================================ */

            const submitButton =
                form.querySelector(
                    'button[type="submit"]'
                );


            if (submitButton) {
                submitButton.disabled = true;
            }


            try {

                console.log(
                    "Sending AI question..."
                );


                console.log(
                    "Question:",
                    question
                );


                console.log(
                    "Kundli:",
                    result
                );


                /* ========================================
                   SEND REQUEST TO FLASK
                ======================================== */

                const response =
                    await fetch(
                        AI_API_URL,
                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"

                            },

                            body:
                                JSON.stringify({

                                    question:
                                        question,

                                    kundli:
                                        result

                                })

                        }
                    );


                /* ========================================
                   READ RESPONSE
                ======================================== */

                let data;


                try {

                    data =
                        await response.json();

                } catch (jsonError) {

                    throw new Error(
                        "Server returned an invalid JSON response."
                    );
                }


                console.log(
                    "AI API response:",
                    data
                );


                /* ========================================
                   CHECK RESPONSE
                ======================================== */

                if (
                    !response.ok ||
                    data.success !== true
                ) {

                    throw new Error(

                        data.message ||

                        data.error ||

                        data.details ||

                        "AI could not generate an answer."

                    );
                }


                const answer =
                    data.answer;


                if (!answer) {

                    throw new Error(
                        "AI returned an empty answer."
                    );
                }


                /* ========================================
                   DISPLAY ANSWER
                ======================================== */

                if (loading) {

                    loading.innerHTML = `

                        <strong>
                            AI Jyotish
                        </strong>

                        <p>
                            ${formatAIAnswer(
                                answer
                            )}
                        </p>

                    `;
                }


                /* ========================================
                   SCROLL
                ======================================== */

                messages.lastElementChild?.scrollIntoView({

                    behavior: "smooth",

                    block: "nearest"

                });


            } catch (error) {

                console.error(
                    "AI Error:",
                    error
                );


                if (loading) {

                    loading.innerHTML = `

                        <strong>
                            AI Jyotish
                        </strong>

                        <p>
                            Sorry, I couldn't generate
                            an answer right now.
                        </p>

                        <p class="muted">
                            ${escapeHTML(
                                error.message
                            )}
                        </p>

                    `;
                }

            } finally {

                if (submitButton) {
                    submitButton.disabled = false;
                }
            }

        }
    );
}


/* =========================================================
   FORMAT AI ANSWER
========================================================= */

function formatAIAnswer(text) {

    if (
        text === null ||
        text === undefined
    ) {
        return "";
    }

    return escapeHTML(
        String(text)
    )
    .replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    )
    .replace(
        /\n/g,
        "<br>"
    );
}


/* =========================================================
   KUNDLI ERROR
========================================================= */

function showKundliError(message) {

    const container =
        getElement(
            "lagnaChart"
        );

    if (!container) {
        return;
    }

    container.innerHTML = `

        <div class="yoga-card">

            <h3>
                Unable to load Kundli
            </h3>

            <p class="muted">
                ${escapeHTML(
                    message
                )}
            </p>

            <br>

            <a
                href="birth-form.html"
                class="primary-button"
            >
                Create Kundli
            </a>

        </div>
    `;
}


/* =========================================================
   HTML ESCAPE
========================================================= */

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


/* =========================================================
   START APPLICATION
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "AI Jyotish JavaScript loaded."
        );

        initializeBirthForm();

        initializeKundliPage();

    }
);