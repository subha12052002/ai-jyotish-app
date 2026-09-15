/**
 * AI Jyotish — Kundli Module
 * --------------------------------
 * Detailed birth-chart analysis presentation.
 *
 * Backend remains the source of truth for all calculations.
 */

(function () {
    "use strict";

    const MODULE_NAME = "AIJyotishKundli";

    const PLANET_SYMBOLS = {
        Sun: "☉",
        Moon: "☽",
        Mars: "♂",
        Mercury: "☿",
        Jupiter: "♃",
        Venus: "♀",
        Saturn: "♄",
        Rahu: "☊",
        Ketu: "☋"
    };

    const PLANET_CLASSES = {
        Sun: "sun",
        Moon: "moon",
        Mars: "mars",
        Mercury: "mercury",
        Jupiter: "jupiter",
        Venus: "venus",
        Saturn: "saturn",
        Rahu: "rahu",
        Ketu: "ketu"
    };

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function value(object, keys, fallback = "—") {
        if (!object || typeof object !== "object") {
            return fallback;
        }

        for (const key of keys) {
            if (
                object[key] !== undefined &&
                object[key] !== null &&
                object[key] !== ""
            ) {
                return object[key];
            }
        }

        return fallback;
    }

    function symbol(planet) {
        return PLANET_SYMBOLS[planet] || "✦";
    }

    function planetClass(planet) {
        return PLANET_CLASSES[planet] || "";
    }

    function titleCase(valueText) {
        if (!valueText || typeof valueText !== "string") {
            return valueText || "—";
        }

        return valueText
            .replace(/[_-]/g, " ")
            .replace(/\s+/g, " ")
            .trim()
            .replace(/\b\w/g, letter => letter.toUpperCase());
    }

    function formatNumber(number, digits = 2) {
        const parsed = Number(number);

        if (!Number.isFinite(parsed)) {
            return number ?? "—";
        }

        return parsed.toFixed(digits);
    }

    function getAnalysis(chart) {
        return chart?.analysis || {};
    }

    function renderAnalysisStatus(chart, container) {
        const analysis = getAnalysis(chart);

        if (!container) {
            return;
        }

        const summary =
            analysis.summary ||
            analysis.analysis_summary ||
            {};

        const completed =
            value(
                summary,
                ["completed_modules", "completedModules"],
                null
            );

        const total =
            value(
                summary,
                ["total_modules", "totalModules"],
                null
            );

        const percentage =
            value(
                summary,
                ["completion_percentage", "completionPercentage"],
                null
            );

        const status =
            value(
                summary,
                ["status", "message"],
                "Complete analysis generated"
            );

        let scoreText = "";

        if (percentage !== null && percentage !== "—") {
            scoreText = `${formatNumber(percentage, 0)}%`;
        } else if (
            completed !== null &&
            total !== null
        ) {
            scoreText = `${completed}/${total}`;
        }

        container.innerHTML = `
            <div class="analysis-status-card">
                <div class="analysis-status-icon">✦</div>

                <div class="analysis-status-content">
                    <span class="analysis-eyebrow">
                        COMPLETE CHART ANALYSIS
                    </span>

                    <h3>
                        ${escapeHtml(status)}
                    </h3>

                    ${
                        scoreText
                            ? `
                                <p>
                                    Calculation coverage:
                                    <strong>
                                        ${escapeHtml(scoreText)}
                                    </strong>
                                </p>
                            `
                            : ""
                    }
                </div>

                <div class="analysis-status-mark">
                    ✓
                </div>
            </div>
        `;
    }

    function normalizeCollection(data) {
        if (!data) {
            return [];
        }

        if (Array.isArray(data)) {
            return data;
        }

        if (typeof data === "object") {
            return Object.entries(data).map(
                ([name, details]) => {
                    if (
                        details &&
                        typeof details === "object" &&
                        !Array.isArray(details)
                    ) {
                        return {
                            name,
                            ...details
                        };
                    }

                    return {
                        name,
                        value: details
                    };
                }
            );
        }

        return [];
    }

    function renderGenericTable(data, options = {}) {
        const rows = normalizeCollection(data);

        if (!rows.length) {
            return `
                <div class="analysis-empty-inline">
                    No detailed data available.
                </div>
            `;
        }

        const preferredKeys =
            options.keys ||
            [
                "name",
                "planet",
                "sign",
                "house",
                "degree",
                "longitude",
                "status",
                "description",
                "meaning",
                "result"
            ];

        return `
            <div class="analysis-table-wrap">
                <table class="analysis-table">
                    <thead>
                        <tr>
                            ${preferredKeys.map(key => `
                                <th>
                                    ${escapeHtml(titleCase(key))}
                                </th>
                            `).join("")}
                        </tr>
                    </thead>

                    <tbody>
                        ${rows.map(row => `
                            <tr>
                                ${preferredKeys.map(key => {
                                    let cell =
                                        row?.[key];

                                    if (
                                        cell === undefined ||
                                        cell === null
                                    ) {
                                        cell = "—";
                                    }

                                    if (
                                        typeof cell === "object"
                                    ) {
                                        cell =
                                            JSON.stringify(
                                                cell
                                            );
                                    }

                                    return `
                                        <td>
                                            ${escapeHtml(
                                                cell
                                            )}
                                        </td>
                                    `;
                                }).join("")}
                            </tr>
                        `).join("")}
                    </tbody>
                </table>
            </div>
        `;
    }

    function renderPlanetAnalysis(chart) {
        const data =
            getAnalysis(chart).planet_analysis ||
            getAnalysis(chart).planetAnalysis ||
            getAnalysis(chart).planets ||
            chart?.planet_analysis ||
            chart?.planetAnalysis;

        const rows = normalizeCollection(data);

        if (!rows.length) {
            return "";
        }

        return `
            <section class="analysis-panel">
                <div class="analysis-section-heading drishti-heading">

    <div class="analysis-section-icon drishti-icon">
        ◇
    </div>

    <div class="analysis-section-title">
        <span>PLANETARY ASPECTS</span>
        <h3>Drishti Analysis</h3>
    </div>

</div>

                <div class="planet-analysis-grid">
                    ${rows.map(row => {
                        const planet =
                            value(
                                row,
                                [
                                    "planet",
                                    "name",
                                    "body"
                                ],
                                "Planet"
                            );

                        const sign =
                            value(
                                row,
                                [
                                    "sign",
                                    "rashi"
                                ]
                            );

                        const house =
                            value(
                                row,
                                [
                                    "house",
                                    "house_number",
                                    "houseNumber"
                                ]
                            );

                        const degree =
                            value(
                                row,
                                [
                                    "degree",
                                    "degrees",
                                    "longitude"
                                ]
                            );

                        const interpretation =
                            value(
                                row,
                                [
                                    "interpretation",
                                    "description",
                                    "meaning",
                                    "analysis",
                                    "result"
                                ],
                                ""
                            );

                        return `
                            <article class="planet-analysis-card">
                                <div class="planet-analysis-top">
                                    <div class="planet-analysis-symbol ${planetClass(
                                        planet
                                    )}">
                                        ${escapeHtml(
                                            symbol(planet)
                                        )}
                                    </div>

                                    <div>
                                        <span>
                                            ${escapeHtml(
                                                titleCase(
                                                    planet
                                                )
                                            )}
                                        </span>

                                        <strong>
                                            ${escapeHtml(
                                                sign
                                            )}
                                        </strong>
                                    </div>
                                </div>

                                <div class="planet-analysis-meta">
                                    <span>
                                        House:
                                        <strong>
                                            ${escapeHtml(
                                                house
                                            )}
                                        </strong>
                                    </span>

                                    <span>
                                        Degree:
                                        <strong>
                                            ${escapeHtml(
                                                formatNumber(
                                                    degree,
                                                    2
                                                )
                                            )}
                                        </strong>
                                    </span>
                                </div>

                                ${
                                    interpretation !== ""
                                        ? `
                                            <p>
                                                ${escapeHtml(
                                                    interpretation
                                                )}
                                            </p>
                                        `
                                        : ""
                                }
                            </article>
                        `;
                    }).join("")}
                </div>
            </section>
        `;
    }

    function renderNakshatraAnalysis(chart) {
        const data =
            getAnalysis(chart).nakshatra_analysis ||
            getAnalysis(chart).nakshatraAnalysis ||
            getAnalysis(chart).nakshatra;

        if (!data) {
            return "";
        }

        const name =
            value(
                data,
                ["name", "nakshatra"],
                value(
                    chart,
                    [
                        "birth_nakshatra",
                        "birthNakshatra",
                        "nakshatra"
                    ]
                )
            );

        const lord =
            value(
                data,
                [
                    "lord",
                    "nakshatra_lord",
                    "nakshatraLord"
                ],
                value(
                    chart,
                    [
                        "birth_nakshatra_lord",
                        "birthNakshatraLord"
                    ]
                )
            );

        const pada =
            value(
                data,
                ["pada", "quarter"],
                value(
                    chart,
                    ["birth_pada", "birthPada"]
                )
            );

        const interpretation =
            value(
                data,
                [
                    "interpretation",
                    "description",
                    "meaning",
                    "analysis"
                ],
                ""
            );

        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ✦
                    </div>

                    <div>
                        <span>NAKSHATRA ANALYSIS</span>
                        <h3>
                            ${escapeHtml(name)}
                        </h3>
                    </div>
                </div>

                <div class="nakshatra-analysis-grid">
                    <div>
                        <span>Nakshatra Lord</span>
                        <strong>
                            ${escapeHtml(lord)}
                        </strong>
                    </div>

                    <div>
                        <span>Pada</span>
                        <strong>
                            ${escapeHtml(pada)}
                        </strong>
                    </div>
                </div>

                ${
                    interpretation
                        ? `
                            <div class="analysis-highlight">
                                <span>✦</span>
                                <p>
                                    ${escapeHtml(
                                        interpretation
                                    )}
                                </p>
                            </div>
                        `
                        : ""
                }
            </section>
        `;
    }
function renderAspects(chart) {

    const analysis = getAnalysis(chart) || {};

    const wrapper =
        analysis.aspects ||
        analysis.planetary_aspects ||
        analysis.planetaryAspects;

    if (!wrapper) {
        return "";
    }

    const data =
        wrapper.data ||
        wrapper;

    const planetSummary =
        data.by_planet ||
        {};

    const planetNames = Object.keys(planetSummary);

    if (!planetNames.length) {
        return `
            <section class="analysis-panel">

                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ◇
                    </div>

                    <div>
                        <span>PLANETARY ASPECTS</span>
                        <h3>Drishti Analysis</h3>
                    </div>
                </div>

                <p class="analysis-empty">
                    Planetary aspect data unavailable.
                </p>

            </section>
        `;
    }

    const rows = planetNames.map((planet, index) => {

        const info =
            planetSummary[planet] || {};

        const casts =
            Array.isArray(info.casts)
                ? info.casts
                : [];

        const aspectNames = casts.map(aspect =>
            aspect.aspect_name ||
            `${aspect.aspect_number}th Aspect`
        );

        const houses = casts.map(aspect =>
            `House ${aspect.target_house}`
        );

        return {
            rank: index + 1,
            planet,
            aspects: aspectNames.join(", "),
            houses: houses.join(", ")
        };

    });

    return `
        <section class="analysis-panel">

            <div class="analysis-panel-heading">

                <div class="analysis-panel-icon">
                    ◇
                </div>

                <div>
                    <span>PLANETARY ASPECTS</span>
                    <h3>Drishti Analysis</h3>
                </div>

            </div>

            <div class="analysis-table-wrap">

                <table class="analysis-table aspects-table">

                    <thead>
                        <tr>
                            <th>RANK</th>
                            <th>PLANET</th>
                            <th>ASPECTS CAST</th>
                            <th>HOUSES ASPECTED</th>
                        </tr>
                    </thead>

                    <tbody>

                        ${rows.map(row => `
                            <tr>

                                <td>
                                    <strong>
                                        ${row.rank}
                                    </strong>
                                </td>

                                <td>
                                    <strong>
                                        ${escapeHtml(row.planet)}
                                    </strong>
                                </td>

                                <td>
                                    ${escapeHtml(row.aspects)}
                                </td>

                                <td>
                                    ${escapeHtml(row.houses)}
                                </td>

                            </tr>
                        `).join("")}

                    </tbody>

                </table>

            </div>

        </section>
    `;
}
function renderVababal(chart) {

    const analysis = getAnalysis(chart) || {};

    // New Bhava Bala module
    const wrapper =
        analysis.bhava_bala ||
        analysis.bhavabala ||
        analysis.bhavaBala;

    if (!wrapper) {
        return `
            <section class="analysis-panel">

                <div class="analysis-section-heading">

    <div class="analysis-section-icon">
        ◉
    </div>

    <div class="analysis-section-title">
        <span>PLANETARY ASPECTS</span>
        <h3>Drishti Analysis</h3>
    </div>

</div>

                <p class="analysis-empty">
                    Bhava Bala data unavailable.
                </p>

            </section>
        `;
    }

    // Handle analysis-engine wrapper
    const data =
        wrapper.data ||
        wrapper;

    // New Bhava Bala module normally provides table
    const table =
        data.table ||
        data.bhava_bala_table ||
        data.bhavaBalaTable ||
        [];

    if (!Array.isArray(table) || !table.length) {
        return `
            <section class="analysis-panel">

                <div class="analysis-panel-heading">

                    <div class="analysis-panel-icon">
                        ♜
                    </div>

                    <div>
                        <span>VABABAL / BHAVA BALA</span>
                        <h3>House Strength</h3>
                    </div>

                </div>

                <p class="analysis-empty">
                    Bhava Bala data unavailable.
                </p>

            </section>
        `;
    }

    return `
        <section class="analysis-panel">

            <div class="analysis-panel-heading">

                <div class="analysis-panel-icon">
                    ♜
                </div>

                <div>
                    <span>VABABAL / BHAVA BALA</span>
                    <h3>House Strength</h3>
                </div>

            </div>

            <div class="analysis-table-wrap">

                <table class="analysis-table">

                    <thead>

                        <tr>
                            <th>RANK</th>
                            <th>HOUSE</th>
                            <th>BHAVADHIPATI BALA</th>
                            <th>BHAVA DIG BALA</th>
                            <th>BHAVA DRSHTI BALA</th>
                            <th>TOTAL</th>
                            <th>RUPAS</th>
                        </tr>

                    </thead>

                    <tbody>

                        ${table.map(row => {

                            return `
                                <tr>

                                    <td>
                                        <strong>
                                            ${escapeHtml(
                                                row.rank ?? "—"
                                            )}
                                        </strong>
                                    </td>

                                    <td>
    <strong>
        ${(() => {
            const n = Number(row.house);

            if (!Number.isFinite(n)) {
                return "—";
            }

            const suffix =
                n % 100 >= 11 && n % 100 <= 13
                    ? "th"
                    : n % 10 === 1
                        ? "st"
                        : n % 10 === 2
                            ? "nd"
                            : n % 10 === 3
                                ? "rd"
                                : "th";

            return `${n}${suffix}`;
        })()}
    </strong>
</td>
                                    <td>
                                        ${escapeHtml(
                                            Number(
                                                row.bhavadhipati_bala ?? 0
                                            ).toFixed(2)
                                        )}
                                    </td>

                                    <td>
                                        ${escapeHtml(
                                            Number(
                                                row.bhava_dig_bala ?? 0
                                            ).toFixed(2)
                                        )}
                                    </td>

                                    <td>
                                        ${escapeHtml(
                                            Number(
                                                row.bhava_drishti_bala ?? 0
                                            ).toFixed(2)
                                        )}
                                    </td>

                                    <td>
                                        <strong>
                                            ${escapeHtml(
                                                Number(
                                                    row.total_bhava_bala ??
                                                    row.total ??
                                                    0
                                                ).toFixed(2)
                                            )}
                                        </strong>
                                    </td>

                                    <td>
                                        ${escapeHtml(
                                            Number(
                                                row.bhava_bala_rupas ??
                                                row.rupas ??
                                                0
                                            ).toFixed(2)
                                        )}
                                    </td>

                                </tr>
                            `;

                        }).join("")}

                    </tbody>

                </table>

            </div>

        </section>
    `;
}

    function renderDignity(chart) {
        const data =
            getAnalysis(chart).dignity ||
            getAnalysis(chart).dignities ||
            getAnalysis(chart).planetary_dignity;

        if (!data) {
            return "";
        }

        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ♕
                    </div>

                    <div>
                        <span>PLANETARY DIGNITY</span>
                        <h3>Strength & Dignity</h3>
                    </div>
                </div>

                ${renderGenericTable(data, {
                    keys: [
                        "planet",
                        "sign",
                        "dignity",
                        "status",
                        "strength",
                        "description"
                    ]
                })}
            </section>
        `;
    }

    function renderCombustion(chart) {
        const data =
            getAnalysis(chart).combustion ||
            getAnalysis(chart).combust ||
            getAnalysis(chart).combust_planets;

        if (!data) {
            return "";
        }

        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ☉
                    </div>

                    <div>
                        <span>COMBUSTION</span>
                        <h3>Planetary Combustion</h3>
                    </div>
                </div>

                ${renderGenericTable(data, {
                    keys: [
                        "planet",
                        "status",
                        "distance",
                        "orb",
                        "description"
                    ]
                })}
            </section>
        `;
    }
function renderShadbala(chart) {
    const analysis = getAnalysis(chart);

    const module =
        analysis.shadbala ||
        analysis.shad_bala ||
        analysis.planetary_strength;

    if (!module) {
        return "";
    }

    // Backend response:
    // analysis.shadbala.data.table
    const rows =
        Array.isArray(module.table)
            ? module.table
            : Array.isArray(module.data?.table)
                ? module.data.table
                : [];

    if (!rows.length) {
        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">✦</div>

                    <div>
                        <span>SHADBALA</span>
                        <h3>Six-Fold Planetary Strength</h3>
                    </div>
                </div>

                <div class="analysis-empty-inline">
                    No Shadbala data available.
                </div>
            </section>
        `;
    }

    // Rank strongest → weakest
    // Rank by Total Rupas: highest → lowest
const rankedRows = [...rows]
    .sort((a, b) => {
        const rupasA = Number(a?.total_rupas);
        const rupasB = Number(b?.total_rupas);

        // Valid Rupas always come before missing/invalid values
        if (!Number.isFinite(rupasA) && !Number.isFinite(rupasB)) {
            return 0;
        }

        if (!Number.isFinite(rupasA)) {
            return 1;
        }

        if (!Number.isFinite(rupasB)) {
            return -1;
        }

        return rupasB - rupasA;
    })
    .map((row, index) => ({
        ...row,
        rank: index + 1
    }));

    const formatBala = value => {
        const number = Number(value);

        return Number.isFinite(number)
            ? number.toFixed(2)
            : "—";
    };

    const formatRupas = value => {
        const number = Number(value);

        return Number.isFinite(number)
            ? number.toFixed(2)
            : "—";
    };

    return `
        <section class="analysis-panel shadbala-panel">

            <div class="analysis-panel-heading">
                <div class="analysis-panel-icon">
                    ✦
                </div>

                <div>
                    <span>SHADBALA</span>
                    <h3>Six-Fold Planetary Strength</h3>
                </div>
            </div>

            <div class="analysis-table-wrap shadbala-table-wrap">

                <table class="analysis-table shadbala-table">

                    <thead>
                        <tr>
                            <th>RANK</th>
                            <th>PLANET</th>
                            <th>STHANA</th>
                            <th>DIG</th>
                            <th>KALA</th>
                            <th>CHESHTA</th>
                            <th>NATURAL</th>
                            <th>DRIK</th>
                            <th>TOTAL</th>
                            <th>RUPAS</th>
                        </tr>
                    </thead>

                    <tbody>
                        ${rankedRows.map(row => {

                            const planet =
                                escapeHtml(
                                    row?.planet || "—"
                                );

                            const planetSymbol =
                                symbol(row?.planet);

                            const planetClassName =
                                planetClass(row?.planet);

                            return `
                                <tr>

                                    <td class="shadbala-rank">
                                        ${row.rank}
                                    </td>

                                    <td class="shadbala-planet">
                                        <span class="planet-symbol ${planetClassName}">
                                            ${planetSymbol}
                                        </span>

                                        <span>
                                            ${planet}
                                        </span>
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.sthana_bala
                                        )}
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.dig_bala
                                        )}
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.kala_bala
                                        )}
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.cheshta_bala
                                        )}
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.naisargika_bala
                                        )}
                                    </td>

                                    <td>
                                        ${formatBala(
                                            row?.drik_bala
                                        )}
                                    </td>

                                    <td class="shadbala-total">
                                        ${formatBala(
                                            row?.total_shashtiamsas
                                        )}
                                    </td>

                                    <td class="shadbala-rupas">
                                        ${formatRupas(
                                            row?.total_rupas
                                        )}
                                    </td>

                                </tr>
                            `;
                        }).join("")}
                    </tbody>

                </table>

            </div>
        </section>
    `;
}          
    function renderAshtakavarga(chart) {
        const data =
            getAnalysis(chart).ashtakavarga ||
            getAnalysis(chart).ashta_kavarga ||
            getAnalysis(chart).ashtakavarga_analysis;

        if (!data) {
            return "";
        }

        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ◈
                    </div>

                    <div>
                        <span>ASHTAKAVARGA</span>
                        <h3>Planetary Point Analysis</h3>
                    </div>
                </div>

                ${renderGenericTable(data)}
            </section>
        `;
    }

    function renderNavamsa(chart) {
        const data =
            getAnalysis(chart).navamsa ||
            getAnalysis(chart).navamsha ||
            chart?.navamsa;

        if (!data) {
            return "";
        }

        return `
            <section class="analysis-panel">
                <div class="analysis-panel-heading">
                    <div class="analysis-panel-icon">
                        ⌘
                    </div>

                    <div>
                        <span>NAVAMSA</span>
                        <h3>D9 Divisional Analysis</h3>
                    </div>
                </div>

                ${renderGenericTable(data, {
                    keys: [
                        "planet",
                        "sign",
                        "degree",
                        "navamsa",
                        "house",
                        "status"
                    ]
                })}
            </section>
        `;
    }

    function renderCompleteAnalysis(chart) {

    const container =
        document.getElementById("completeAnalysis");

    if (!container || !chart) {
        return;
    }

    const analysis =
        getAnalysis(chart);

    if (!Object.keys(analysis).length) {
        container.innerHTML = "";
        return;
    }

    container.innerHTML = `

    <div class="complete-analysis-header">

    <div class="complete-analysis-icon">
        ✦
    </div>

    <div class="complete-analysis-title">
        <span>DEEP VEDIC ANALYSIS</span>
        <h2>Complete Birth Chart Analysis</h2>
        <p>
            Planetary aspects, Bhava Bala and Shadbala derived from your birth chart.
        </p>
    </div>

</div>

        <div class="complete-analysis-sections">

            ${renderAspects(chart)}

            ${renderVababal(chart)}

            ${renderShadbala(chart)}

        </div>

    `;
}

    function render(chart) {
        renderCompleteAnalysis(chart);
    }

   window[MODULE_NAME] = {
    render,
    renderCompleteAnalysis,
    renderAspects,
    renderVababal,
    renderShadbala
};
})();