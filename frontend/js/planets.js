(function () {
    "use strict";

    /*
     * AI Jyotish — Planetary Intelligence
     *
     * Frontend-only rendering helpers.
     * Planetary calculations remain completely backend-driven.
     */

    const PLANETS = {
        Sun: {
            symbol: "☉",
            hindi: "Surya",
            colorClass: "planet-sun",
            keywords: ["identity", "authority", "confidence"]
        },

        Moon: {
            symbol: "☽",
            hindi: "Chandra",
            colorClass: "planet-moon",
            keywords: ["mind", "emotions", "intuition"]
        },

        Mars: {
            symbol: "♂",
            hindi: "Mangal",
            colorClass: "planet-mars",
            keywords: ["energy", "courage", "action"]
        },

        Mercury: {
            symbol: "☿",
            hindi: "Budha",
            colorClass: "planet-mercury",
            keywords: ["intelligence", "communication", "logic"]
        },

        Jupiter: {
            symbol: "♃",
            hindi: "Guru",
            colorClass: "planet-jupiter",
            keywords: ["wisdom", "growth", "fortune"]
        },

        Venus: {
            symbol: "♀",
            hindi: "Shukra",
            colorClass: "planet-venus",
            keywords: ["love", "beauty", "relationships"]
        },

        Saturn: {
            symbol: "♄",
            hindi: "Shani",
            colorClass: "planet-saturn",
            keywords: ["discipline", "karma", "responsibility"]
        },

        Rahu: {
            symbol: "☊",
            hindi: "Rahu",
            colorClass: "planet-rahu",
            keywords: ["desire", "ambition", "material growth"]
        },

        Ketu: {
            symbol: "☋",
            hindi: "Ketu",
            colorClass: "planet-ketu",
            keywords: ["detachment", "spirituality", "intuition"]
        }
    };

    const SIGN_NAMES = [
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

    const SIGN_SYMBOLS = [
        "♈",
        "♉",
        "♊",
        "♋",
        "♌",
        "♍",
        "♎",
        "♏",
        "♐",
        "♑",
        "♒",
        "♓"
    ];

    function escapeHTML(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function toNumber(value) {
        const n = Number(value);
        return Number.isFinite(n) ? n : null;
    }

    function normalizeName(value) {
        return String(value || "")
            .trim()
            .toLowerCase();
    }

    function getPlanetName(planet) {
        if (!planet) return "";

        if (typeof planet === "string") {
            return planet;
        }

        return (
            planet.name ||
            planet.planet ||
            planet.body ||
            ""
        );
    }

    function getPlanets(chart) {
        if (!chart) return [];

        let source =
            chart.planets ||
            chart.planet_positions ||
            chart.planetPositions ||
            chart.bodies ||
            [];

        if (
            source &&
            typeof source === "object" &&
            !Array.isArray(source)
        ) {
            return Object.entries(source).map(
                ([name, value]) => ({
                    ...(value &&
                    typeof value === "object"
                        ? value
                        : { value }),

                    name:
                        value?.name ||
                        value?.planet ||
                        name
                })
            );
        }

        return Array.isArray(source)
            ? source
            : [];
    }

    function findPlanet(chart, planetName) {
        const target =
            normalizeName(planetName);

        return getPlanets(chart).find(
            (planet) =>
                normalizeName(
                    getPlanetName(planet)
                ) === target
        );
    }

    function getSignIndex(planet) {
        if (!planet) return null;

        const candidates = [
            planet.sign_index,
            planet.signIndex,
            planet.rashi_index,
            planet.rashiIndex,
            planet.zodiac_index,
            planet.signNumber
        ];

        for (const value of candidates) {
            const n = toNumber(value);

            if (
                n !== null &&
                n >= 0 &&
                n <= 11
            ) {
                return Math.floor(n);
            }

            if (
                n !== null &&
                n >= 1 &&
                n <= 12
            ) {
                return Math.floor(n - 1);
            }
        }

        const text =
            normalizeName(
                planet.sign ||
                planet.rashi ||
                planet.zodiac
            );

        const index =
            SIGN_NAMES.findIndex(
                (name) =>
                    normalizeName(name) === text
            );

        return index >= 0
            ? index
            : null;
    }

    function getSignName(planet) {
        const index =
            getSignIndex(planet);

        if (index === null) {
            return (
                planet?.sign ||
                planet?.rashi ||
                "—"
            );
        }

        return SIGN_NAMES[index];
    }

    function getDegree(planet) {
        if (!planet) return null;

        const candidates = [
            planet.degree,
            planet.degrees,
            planet.degree_in_sign,
            planet.degreeInSign
        ];

        for (const value of candidates) {
            const n = toNumber(value);

            if (
                n !== null &&
                n >= 0 &&
                n < 30
            ) {
                return n;
            }
        }

        const longitude =
            getLongitude(planet);

        if (longitude !== null) {
            return (
                ((longitude % 30) + 30) %
                30
            );
        }

        return null;
    }

    function getLongitude(planet) {
        if (!planet) return null;

        const candidates = [
            planet.longitude,
            planet.longitude_deg,
            planet.absolute_longitude,
            planet.absoluteLongitude
        ];

        for (const value of candidates) {
            const n = toNumber(value);

            if (n !== null) {
                return n;
            }
        }

        return null;
    }

    function getHouse(planet) {
        if (!planet) return null;

        const candidates = [
            planet.house,
            planet.house_number,
            planet.houseNumber,
            planet.bhava
        ];

        for (const value of candidates) {
            const n = toNumber(value);

            if (
                n !== null &&
                n >= 1 &&
                n <= 12
            ) {
                return Math.floor(n);
            }
        }

        return null;
    }

    function getNakshatra(planet) {
        if (!planet) return null;

        const direct =
            planet.nakshatra ||
            planet.nakshatra_name ||
            planet.nakshatraName ||
            null;

        if (direct) return direct;

        const longitude = getLongitude(planet);
        const nakshatraModule = window.AIJyotishNakshatra;

        if (longitude !== null && nakshatraModule &&
            typeof nakshatraModule.getNakshatraData === "function") {
            return nakshatraModule.getNakshatraData(planet)?.name || null;
        }

        return null;
    }

    function getPada(planet) {
        if (!planet) return null;

        const value =
            planet.pada ??
            planet.nakshatra_pada ??
            planet.nakshatraPada;

        const n = toNumber(value);
        if (n !== null) return Math.floor(n);

        const nakshatraModule = window.AIJyotishNakshatra;
        const longitude = getLongitude(planet);

        if (longitude !== null && nakshatraModule &&
            typeof nakshatraModule.getNakshatraData === "function") {
            return nakshatraModule.getNakshatraData(planet)?.pada || null;
        }

        return value || null;
    }

    function getNakshatraLord(planet) {
        if (!planet) return null;

        const direct =
            planet.nakshatra_lord ||
            planet.nakshatraLord ||
            null;

        if (direct) return direct;

        const nakshatraModule = window.AIJyotishNakshatra;
        if (nakshatraModule &&
            typeof nakshatraModule.getNakshatraData === "function") {
            return nakshatraModule.getNakshatraData(planet)?.lord ||
                planet.lord || null;
        }

        return planet.lord || null;
    }

    function getStatus(planet) {
        if (!planet) return "—";

        if (
            planet.status &&
            typeof planet.status === "string"
        ) {
            return planet.status;
        }

        const statuses = [];

        if (
            planet.retrograde === true ||
            planet.is_retrograde === true
        ) {
            statuses.push("Retrograde");
        }

        if (
            planet.combust === true ||
            planet.is_combust === true
        ) {
            statuses.push("Combust");
        }

        if (
            planet.exalted === true ||
            planet.is_exalted === true
        ) {
            statuses.push("Exalted");
        }

        if (
            planet.debilitated === true ||
            planet.is_debilitated === true
        ) {
            statuses.push("Debilitated");
        }

        return statuses.length
            ? statuses.join(" • ")
            : "Normal";
    }

    function getDignity(planet) {
        if (!planet) return null;

        return (
            planet.dignity ||
            planet.dignity_status ||
            planet.dignityStatus ||
            null
        );
    }

    function getDescription(planetName) {
        const data =
            PLANETS[planetName];

        if (!data) {
            return "";
        }

        return data.keywords.join(" • ");
    }

    function getPlanetData(
        chart,
        planetName
    ) {
        const planet =
            findPlanet(
                chart,
                planetName
            );

        if (!planet) {
            return null;
        }

        const signIndex =
            getSignIndex(planet);

        return {
            raw: planet,
            name: planetName,

            symbol:
                PLANETS[planetName]?.symbol ||
                planetName.slice(0, 2),

            hindi:
                PLANETS[planetName]?.hindi ||
                "",

            colorClass:
                PLANETS[planetName]?.colorClass ||
                "planet-default",

            sign:
                getSignName(planet),

            signIndex,

            signSymbol:
                signIndex !== null
                    ? SIGN_SYMBOLS[
                        signIndex
                    ]
                    : "",

            degree:
                getDegree(planet),

            longitude:
                getLongitude(planet),

            house:
                getHouse(planet),

            nakshatra:
                getNakshatra(planet),

            pada:
                getPada(planet),

            nakshatraLord:
                getNakshatraLord(
                    planet
                ),

            status:
                getStatus(planet),

            dignity:
                getDignity(planet),

            description:
                getDescription(
                    planetName
                )
        };
    }

    function formatDegree(value) {
        return value === null
            ? "—"
            : `${value.toFixed(2)}°`;
    }

    function formatLongitude(value) {
        return value === null
            ? "—"
            : `${value.toFixed(2)}°`;
    }

    function renderPlanetCard(
        planetData
    ) {
        if (!planetData) return "";

        const {
            name,
            symbol,
            hindi,
            colorClass,
            sign,
            signSymbol,
            degree,
            house,
            nakshatra,
            pada,
            nakshatraLord,
            status,
            dignity,
            description
        } = planetData;

        return `
            <article
                class="planet-card ${escapeHTML(colorClass)}"
                data-planet="${escapeHTML(name)}"
            >
                <div class="planet-card-top">
                    <div class="planet-symbol-wrap">
                        <span class="planet-symbol">
                            ${escapeHTML(symbol)}
                        </span>
                    </div>

                    <div class="planet-title">
                        <h3>
                            ${escapeHTML(name)}
                        </h3>

                        <span>
                            ${escapeHTML(hindi)}
                        </span>
                    </div>

                    <span class="planet-status">
                        ${escapeHTML(status)}
                    </span>
                </div>

                <div class="planet-placement">
                    <div class="planet-sign">
                        <span class="planet-sign-symbol">
                            ${escapeHTML(signSymbol)}
                        </span>

                        <div>
                            <small>Rashi</small>
                            <strong>
                                ${escapeHTML(sign)}
                            </strong>
                        </div>
                    </div>

                    <div class="planet-degree">
                        <small>Degree</small>
                        <strong>
                            ${formatDegree(degree)}
                        </strong>
                    </div>

                    <div class="planet-house">
                        <small>House</small>
                        <strong>
                            ${
                                house
                                    ? house
                                    : "—"
                            }
                        </strong>
                    </div>
                </div>

                <div class="planet-meta">
                    ${
                        nakshatra
                            ? `
                                <div>
                                    <span>Nakshatra</span>
                                    <strong>
                                        ${escapeHTML(nakshatra)}
                                    </strong>
                                </div>
                            `
                            : ""
                    }

                    ${
                        pada
                            ? `
                                <div>
                                    <span>Pada</span>
                                    <strong>
                                        ${escapeHTML(pada)}
                                    </strong>
                                </div>
                            `
                            : ""
                    }

                    ${
                        nakshatraLord
                            ? `
                                <div>
                                    <span>Star Lord</span>
                                    <strong>
                                        ${escapeHTML(nakshatraLord)}
                                    </strong>
                                </div>
                            `
                            : ""
                    }

                    ${
                        dignity
                            ? `
                                <div>
                                    <span>Dignity</span>
                                    <strong>
                                        ${escapeHTML(dignity)}
                                    </strong>
                                </div>
                            `
                            : ""
                    }
                </div>

                <div class="planet-card-footer">
                    <span>
                        ${escapeHTML(description)}
                    </span>
                </div>
            </article>
        `;
    }

    function renderPlanetCards(
        container,
        chart
    ) {
        if (!container) return;

        const cards =
            Object.keys(PLANETS)
                .map(
                    (name) =>
                        getPlanetData(
                            chart,
                            name
                        )
                )
                .filter(Boolean)
                .map(
                    renderPlanetCard
                )
                .join("");

        container.innerHTML =
            cards ||
            `
                <div class="planet-empty">
                    No planetary position data
                    is available.
                </div>
            `;

        return cards;
    }

    function renderPlanetTable(
        container,
        chart
    ) {
        if (!container) return;

        const planets =
            Object.keys(PLANETS)
                .map(
                    (name) =>
                        getPlanetData(
                            chart,
                            name
                        )
                )
                .filter(Boolean);

        if (!planets.length) {
            container.innerHTML = `
                <div class="planet-empty">
                    No planetary data available.
                </div>
            `;

            return;
        }

        container.innerHTML = `
            <div class="planet-table-wrap">
                <table class="planet-details-table">
                    <thead>
                        <tr>
                            <th>Planet</th>
                            <th>Rashi</th>
                            <th>Degree</th>
                            <th>Longitude</th>
                            <th>House</th>
                            <th>Nakshatra</th>
                            <th>Star Lord</th>
                            <th>Pada</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        ${planets.map((planet) => `
                            <tr
                                data-planet="${escapeHTML(planet.name)}"
                            >
                                <td>
                                    <div class="planet-table-name">
                                        <span class="planet-table-symbol">
                                            ${escapeHTML(
                                                planet.symbol
                                            )}
                                        </span>

                                        <strong>
                                            ${escapeHTML(
                                                planet.name
                                            )}
                                        </strong>
                                    </div>
                                </td>

                                <td>
                                    <span class="planet-rashi">
                                        ${escapeHTML(
                                            planet.signSymbol
                                        )}
                                        ${escapeHTML(
                                            planet.sign
                                        )}
                                    </span>
                                </td>

                                <td>
                                    ${formatDegree(
                                        planet.degree
                                    )}
                                </td>

                                <td>
                                    ${formatLongitude(
                                        planet.longitude
                                    )}
                                </td>

                                <td>
                                    ${
                                        planet.house
                                            ? `House ${planet.house}`
                                            : "—"
                                    }
                                </td>

                                <td>
                                    ${
                                        planet.nakshatra
                                            ? escapeHTML(
                                                planet.nakshatra
                                            )
                                            : "—"
                                    }
                                </td>

                                <td>
                                    ${
                                        planet.nakshatraLord
                                            ? escapeHTML(
                                                planet.nakshatraLord
                                            )
                                            : "—"
                                    }
                                </td>

                                <td>
                                    ${
                                        planet.pada
                                            ? escapeHTML(
                                                planet.pada
                                            )
                                            : "—"
                                    }
                                </td>

                                <td>
                                    <span class="planet-status-pill">
                                        ${escapeHTML(
                                            planet.status
                                        )}
                                    </span>
                                </td>
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        `;

        return planets;
    }

    function renderPlanetSummary(
        container,
        chart
    ) {
        if (!container) return;

        const planets =
            Object.keys(PLANETS)
                .map(
                    (name) =>
                        getPlanetData(
                            chart,
                            name
                        )
                )
                .filter(Boolean);

        container.innerHTML = `
            <div class="planet-summary-grid">
                ${planets.map((planet) => `
                    <div class="planet-summary-item">
                        <span
                            class="planet-summary-symbol ${escapeHTML(
                                planet.colorClass
                            )}"
                        >
                            ${escapeHTML(
                                planet.symbol
                            )}
                        </span>

                        <div>
                            <strong>
                                ${escapeHTML(
                                    planet.name
                                )}
                            </strong>

                            <span>
                                ${escapeHTML(
                                    planet.sign
                                )}
                                ${
                                    planet.degree !== null
                                        ? ` · ${planet.degree.toFixed(1)}°`
                                        : ""
                                }
                            </span>
                        </div>
                    </div>
                `).join("")}
            </div>
        `;
    }

    function createPlanetPositionData(
        chart
    ) {
        return Object.keys(PLANETS)
            .map(
                (name) =>
                    getPlanetData(
                        chart,
                        name
                    )
            )
            .filter(Boolean)
            .map((planet) => ({
                planet: planet.name,
                symbol: planet.symbol,
                sign: planet.sign,
                signIndex: planet.signIndex,
                degree: planet.degree,
                longitude: planet.longitude,
                house: planet.house,
                nakshatra: planet.nakshatra,
                pada: planet.pada,
                nakshatraLord:
                    planet.nakshatraLord,
                status: planet.status,
                dignity: planet.dignity
            }));
    }

    function highlightPlanet(
        planetName
    ) {
        const cards =
            document.querySelectorAll(
                `[data-planet="${CSS.escape(
                    planetName
                )}"]`
            );

        cards.forEach((card) => {
            card.classList.add(
                "planet-highlight"
            );

            setTimeout(() => {
                card.classList.remove(
                    "planet-highlight"
                );
            }, 1600);
        });
    }

    function initializePlanetInteractions() {
        document.addEventListener(
            "click",
            (event) => {
                const trigger =
                    event.target.closest(
                        "[data-planet-target]"
                    );

                if (!trigger) return;

                const planet =
                    trigger.getAttribute(
                        "data-planet-target"
                    );

                if (planet) {
                    highlightPlanet(
                        planet
                    );
                }
            }
        );
    }

    const PlanetModule = {
        planets: PLANETS,
        signs: SIGN_NAMES,
        signSymbols: SIGN_SYMBOLS,

        getPlanets,
        findPlanet,
        getPlanetData,
        getSignIndex,
        getSignName,
        getDegree,
        getLongitude,
        getHouse,
        getNakshatra,
        getPada,
        getNakshatraLord,
        getStatus,
        getDignity,

        createPlanetPositionData,

        renderPlanetCard,
        renderPlanetCards,
        renderPlanetTable,
        renderPlanetSummary,

        highlightPlanet
    };

    window.AIJyotishPlanets =
        PlanetModule;

    window.renderPlanetCards =
        renderPlanetCards;

    window.renderPlanetTable =
        renderPlanetTable;

    window.renderPlanetSummary =
        renderPlanetSummary;

    initializePlanetInteractions();
})();