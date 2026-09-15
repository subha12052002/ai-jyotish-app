(function () {
    "use strict";

    /*
     * AI Jyotish — Nakshatra Module
     *
     * Uses the actual Nakshatra data returned by the backend.
     * No astronomical calculations are performed here.
     */

    const NAKSHATRAS = [
        {
            name: "Ashwini",
            lord: "Ketu",
            deity: "Ashwini Kumaras",
            symbol: "🐎",
            range: [0, 13.333333]
        },
        {
            name: "Bharani",
            lord: "Venus",
            deity: "Yama",
            symbol: "🔻",
            range: [13.333333, 26.666667]
        },
        {
            name: "Krittika",
            lord: "Sun",
            deity: "Agni",
            symbol: "🔥",
            range: [26.666667, 40]
        },
        {
            name: "Rohini",
            lord: "Moon",
            deity: "Brahma",
            symbol: "🌸",
            range: [40, 53.333333]
        },
        {
            name: "Mrigashira",
            lord: "Mars",
            deity: "Soma",
            symbol: "🦌",
            range: [53.333333, 66.666667]
        },
        {
            name: "Ardra",
            lord: "Rahu",
            deity: "Rudra",
            symbol: "💧",
            range: [66.666667, 80]
        },
        {
            name: "Punarvasu",
            lord: "Jupiter",
            deity: "Aditi",
            symbol: "🏹",
            range: [80, 93.333333]
        },
        {
            name: "Pushya",
            lord: "Saturn",
            deity: "Brihaspati",
            symbol: "🌼",
            range: [93.333333, 106.666667]
        },
        {
            name: "Ashlesha",
            lord: "Mercury",
            deity: "Nagas",
            symbol: "🐍",
            range: [106.666667, 120]
        },
        {
            name: "Magha",
            lord: "Ketu",
            deity: "Pitris",
            symbol: "👑",
            range: [120, 133.333333]
        },
        {
            name: "Purva Phalguni",
            lord: "Venus",
            deity: "Bhaga",
            symbol: "🛏",
            range: [133.333333, 146.666667]
        },
        {
            name: "Uttara Phalguni",
            lord: "Sun",
            deity: "Aryaman",
            symbol: "☀",
            range: [146.666667, 160]
        },
        {
            name: "Hasta",
            lord: "Moon",
            deity: "Savitar",
            symbol: "✋",
            range: [160, 173.333333]
        },
        {
            name: "Chitra",
            lord: "Mars",
            deity: "Tvashtar",
            symbol: "💎",
            range: [173.333333, 186.666667]
        },
        {
            name: "Swati",
            lord: "Rahu",
            deity: "Vayu",
            symbol: "🌬",
            range: [186.666667, 200]
        },
        {
            name: "Vishakha",
            lord: "Jupiter",
            deity: "Indra-Agni",
            symbol: "🏹",
            range: [200, 213.333333]
        },
        {
            name: "Anuradha",
            lord: "Saturn",
            deity: "Mitra",
            symbol: "🪷",
            range: [213.333333, 226.666667]
        },
        {
            name: "Jyeshtha",
            lord: "Mercury",
            deity: "Indra",
            symbol: "☂",
            range: [226.666667, 240]
        },
        {
            name: "Mula",
            lord: "Ketu",
            deity: "Nirriti",
            symbol: "🌱",
            range: [240, 253.333333]
        },
        {
            name: "Purva Ashadha",
            lord: "Venus",
            deity: "Apas",
            symbol: "💧",
            range: [253.333333, 266.666667]
        },
        {
            name: "Uttara Ashadha",
            lord: "Sun",
            deity: "Vishvedevas",
            symbol: "🏆",
            range: [266.666667, 280]
        },
        {
            name: "Shravana",
            lord: "Moon",
            deity: "Vishnu",
            symbol: "👂",
            range: [280, 293.333333]
        },
        {
            name: "Dhanishta",
            lord: "Mars",
            deity: "Vasus",
            symbol: "🥁",
            range: [293.333333, 306.666667]
        },
        {
            name: "Shatabhisha",
            lord: "Rahu",
            deity: "Varuna",
            symbol: "⭕",
            range: [306.666667, 320]
        },
        {
            name: "Purva Bhadrapada",
            lord: "Jupiter",
            deity: "Aja Ekapada",
            symbol: "⚡",
            range: [320, 333.333333]
        },
        {
            name: "Uttara Bhadrapada",
            lord: "Saturn",
            deity: "Ahir Budhnya",
            symbol: "🐉",
            range: [333.333333, 346.666667]
        },
        {
            name: "Revati",
            lord: "Mercury",
            deity: "Pushan",
            symbol: "🐟",
            range: [346.666667, 360]
        }
    ];

    const NAKSHATRA_TRAITS = {
        "Ashwini": "Quick, energetic, independent and action-oriented.",
        "Bharani": "Strong-willed, responsible, creative and emotionally intense.",
        "Krittika": "Sharp-minded, courageous, disciplined and transformative.",
        "Rohini": "Attractive, artistic, nurturing and comfort-loving.",
        "Mrigashira": "Curious, observant, adaptable and always searching for knowledge.",
        "Ardra": "Intense, analytical, resilient and capable of major transformation.",
        "Punarvasu": "Optimistic, generous, philosophical and able to recover from setbacks.",
        "Pushya": "Nurturing, disciplined, traditional and service-oriented.",
        "Ashlesha": "Perceptive, strategic, intuitive and psychologically deep.",
        "Magha": "Proud, authoritative, traditional and connected with ancestry.",
        "Purva Phalguni": "Creative, sociable, romantic and pleasure-oriented.",
        "Uttara Phalguni": "Reliable, generous, principled and partnership-oriented.",
        "Hasta": "Skillful, intelligent, practical and good with communication.",
        "Chitra": "Creative, charismatic, ambitious and aesthetically inclined.",
        "Swati": "Independent, flexible, diplomatic and freedom-loving.",
        "Vishakha": "Determined, ambitious, focused and goal-oriented.",
        "Anuradha": "Loyal, devoted, organized and capable of deep relationships.",
        "Jyeshtha": "Protective, responsible, intelligent and authoritative.",
        "Mula": "Investigative, fearless, transformative and truth-seeking.",
        "Purva Ashadha": "Confident, persuasive, idealistic and determined.",
        "Uttara Ashadha": "Principled, persistent, responsible and leadership-oriented.",
        "Shravana": "Observant, knowledgeable, communicative and culturally aware.",
        "Dhanishta": "Ambitious, rhythmic, social and materially capable.",
        "Shatabhisha": "Independent, analytical, unconventional and healing-oriented.",
        "Purva Bhadrapada": "Idealistic, intense, philosophical and spiritually inclined.",
        "Uttara Bhadrapada": "Patient, wise, compassionate and emotionally deep.",
        "Revati": "Gentle, imaginative, caring, adaptable and spiritually sensitive."
    };

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
            .toLowerCase()
            .replace(/\s+/g, " ");
    }

    function findNakshatra(name) {
        if (!name) return null;

        const target =
            normalizeName(name);

        return NAKSHATRAS.find(
            (item) =>
                normalizeName(item.name) ===
                target
        ) || null;
    }

    function getNakshatraFromLongitude(
        longitude
    ) {
        const value =
            toNumber(longitude);

        if (value === null) {
            return null;
        }

        const normalized =
            ((value % 360) + 360) %
            360;

        return (
            NAKSHATRAS.find(
                (item) =>
                    normalized >= item.range[0] &&
                    normalized < item.range[1]
            ) || NAKSHATRAS[26]
        );
    }

    function getPadaFromLongitude(
        longitude
    ) {
        const value =
            toNumber(longitude);

        if (value === null) {
            return null;
        }

        const normalized =
            ((value % 360) + 360) %
            360;

        const nakshatra =
            getNakshatraFromLongitude(
                normalized
            );

        if (!nakshatra) {
            return null;
        }

        const relative =
            normalized -
            nakshatra.range[0];

        const pada =
            Math.floor(
                relative /
                3.3333333333333335
            ) + 1;

        return Math.max(
            1,
            Math.min(4, pada)
        );
    }

    function getPlanetList(chart) {
        if (!chart) return [];

        let planets =
            chart.planets ||
            chart.planet_positions ||
            chart.planetPositions ||
            chart.bodies ||
            [];

        if (
            planets &&
            typeof planets === "object" &&
            !Array.isArray(planets)
        ) {
            planets =
                Object.entries(
                    planets
                ).map(
                    ([name, data]) => ({
                        ...(data &&
                        typeof data === "object"
                            ? data
                            : {}),
                        name:
                            data?.name ||
                            data?.planet ||
                            name
                    })
                );
        }

        return Array.isArray(planets)
            ? planets
            : [];
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

    function getLongitude(planet) {
        if (!planet) return null;

        const values = [
            planet.longitude,
            planet.longitude_deg,
            planet.absolute_longitude,
            planet.absoluteLongitude
        ];

        for (const value of values) {
            const n = toNumber(value);

            if (n !== null) {
                return n;
            }
        }

        return null;
    }

    function getNakshatraName(planet) {
        if (!planet) return null;

        return (
            planet.nakshatra ||
            planet.nakshatra_name ||
            planet.nakshatraName ||
            null
        );
    }

    function getLord(planet) {
        if (!planet) return null;

        return (
            planet.nakshatra_lord ||
            planet.nakshatraLord ||
            planet.lord ||
            null
        );
    }

    function getPada(planet) {
        if (!planet) return null;

        const value =
            planet.pada ??
            planet.nakshatra_pada ??
            planet.nakshatraPada;

        const n = toNumber(value);

        return n !== null
            ? Math.floor(n)
            : null;
    }

    function getNakshatraData(
        planet
    ) {
        if (!planet) return null;

        let name =
            getNakshatraName(
                planet
            );

        let longitude =
            getLongitude(
                planet
            );

        let data =
            findNakshatra(name);

        /*
         * Prefer backend-provided Nakshatra.
         * Longitude is only used as a frontend fallback
         * when the backend didn't include the name.
         */
        if (!data && longitude !== null) {
            data =
                getNakshatraFromLongitude(
                    longitude
                );

            name =
                data?.name || null;
        }

        if (!data) {
            return null;
        }

        let pada =
            getPada(planet);

        if (
            !pada &&
            longitude !== null
        ) {
            pada =
                getPadaFromLongitude(
                    longitude
                );
        }

        const lord =
            getLord(planet) ||
            data.lord;

        return {
            name,
            lord,
            deity: data.deity,
            symbol: data.symbol,
            pada,
            longitude,
            traits:
                NAKSHATRA_TRAITS[
                    data.name
                ] || ""
        };
    }

    function findMoon(chart) {
        return getPlanetList(
            chart
        ).find(
            (planet) =>
                normalizeName(
                    getPlanetName(planet)
                ) === "moon"
        );
    }

    function getBirthNakshatra(
        chart
    ) {
        /*
         * The Moon's Nakshatra is the
         * birth Janma Nakshatra in Vedic astrology.
         */
        const moon =
            findMoon(chart);

        if (!moon) {
            return null;
        }

        return getNakshatraData(
            moon
        );
    }

    function renderNakshatraCard(
        container,
        chart
    ) {
        if (!container) return;

        const data =
            getBirthNakshatra(
                chart
            );

        if (!data) {
            container.innerHTML = `
                <div class="nakshatra-empty">
                    <span class="nakshatra-empty-icon">✦</span>
                    <strong>Nakshatra data unavailable</strong>
                    <p>
                        Birth Nakshatra information
                        was not returned with this Kundli.
                    </p>
                </div>
            `;

            return;
        }

        container.innerHTML = `
            <article class="nakshatra-card">
                <div class="nakshatra-card-main">
                    <div class="nakshatra-symbol">
                        ${escapeHTML(
                            data.symbol
                        )}
                    </div>

                    <div class="nakshatra-title">
                        <span>
                            JANMA NAKSHATRA
                        </span>

                        <h3>
                            ${escapeHTML(
                                data.name
                            )}
                        </h3>

                        <p>
                            Moon's birth star
                        </p>
                    </div>

                    <div class="nakshatra-pada">
                        <small>Pada</small>
                        <strong>
                            ${
                                data.pada ||
                                "—"
                            }
                        </strong>
                    </div>
                </div>

                <div class="nakshatra-details">
                    <div>
                        <span>Nakshatra Lord</span>
                        <strong>
                            ${escapeHTML(
                                data.lord
                            )}
                        </strong>
                    </div>

                    <div>
                        <span>Deity</span>
                        <strong>
                            ${escapeHTML(
                                data.deity
                            )}
                        </strong>
                    </div>

                    <div>
                        <span>Traits</span>
                        <strong>
                            ${escapeHTML(
                                data.traits
                            )}
                        </strong>
                    </div>
                </div>
            </article>
        `;

        return data;
    }

    function renderPlanetNakshatras(
        container,
        chart
    ) {
        if (!container) return;

        const planets =
            getPlanetList(
                chart
            );

        const rows =
            planets
                .map((planet) => {
                    const data =
                        getNakshatraData(
                            planet
                        );

                    if (!data) {
                        return "";
                    }

                    return `
                        <div class="nakshatra-planet-row">
                            <div class="nakshatra-planet-name">
                                <span>
                                    ${escapeHTML(
                                        getPlanetName(
                                            planet
                                        )
                                    )}
                                </span>
                            </div>

                            <div class="nakshatra-row-star">
                                <span>
                                    ${escapeHTML(
                                        data.symbol
                                    )}
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        data.name
                                    )}
                                </strong>
                            </div>

                            <div>
                                <span class="nakshatra-row-label">
                                    Lord
                                </span>

                                <strong>
                                    ${escapeHTML(
                                        data.lord
                                    )}
                                </strong>
                            </div>

                            <div>
                                <span class="nakshatra-row-label">
                                    Pada
                                </span>

                                <strong>
                                    ${
                                        data.pada ||
                                        "—"
                                    }
                                </strong>
                            </div>
                        </div>
                    `;
                })
                .filter(Boolean)
                .join("");

        container.innerHTML =
            rows ||
            `
                <div class="nakshatra-empty">
                    No Nakshatra information available.
                </div>
            `;

        return rows;
    }

    function renderNakshatraAnalysis(
        container,
        chart
    ) {
        if (!container) return;

        const birth =
            getBirthNakshatra(
                chart
            );

        if (!birth) {
            container.innerHTML = "";
            return;
        }

        container.innerHTML = `
            <section class="nakshatra-analysis">
                <div class="nakshatra-analysis-heading">
                    <span class="section-eyebrow">
                        VEDIC ASTROLOGY
                    </span>

                    <h3>
                        Your Birth Star
                    </h3>
                </div>

                <div class="nakshatra-analysis-grid">
                    <div class="nakshatra-analysis-star">
                        <span class="nakshatra-analysis-symbol">
                            ${escapeHTML(
                                birth.symbol
                            )}
                        </span>

                        <div>
                            <strong>
                                ${escapeHTML(
                                    birth.name
                                )}
                            </strong>

                            <span>
                                Ruled by
                                ${escapeHTML(
                                    birth.lord
                                )}
                            </span>
                        </div>
                    </div>

                    <div>
                        <span>Deity</span>
                        <strong>
                            ${escapeHTML(
                                birth.deity
                            )}
                        </strong>
                    </div>

                    <div>
                        <span>Pada</span>
                        <strong>
                            ${
                                birth.pada ||
                                "—"
                            }
                        </strong>
                    </div>
                </div>

                ${
                    birth.traits
                        ? `
                            <p class="nakshatra-analysis-text">
                                ${escapeHTML(
                                    birth.traits
                                )}
                            </p>
                        `
                        : ""
                }
            </section>
        `;

        return birth;
    }

    function getAllNakshatras() {
        return NAKSHATRAS.map(
            (item) => ({
                ...item
            })
        );
    }

    const NakshatraModule = {
        nakshatras: NAKSHATRAS,

        findNakshatra,
        getNakshatraFromLongitude,
        getPadaFromLongitude,

        getNakshatraData,
        getBirthNakshatra,

        renderNakshatraCard,
        renderPlanetNakshatras,
        renderNakshatraAnalysis,

        getAllNakshatras
    };

    window.AIJyotishNakshatra =
        NakshatraModule;

    window.renderNakshatraCard =
        renderNakshatraCard;

    window.renderPlanetNakshatras =
        renderPlanetNakshatras;
})();