/**
 * AI Jyotish — Dasha Module
 * --------------------------------
 * Handles Vimshottari Dasha rendering.
 *
 * Backend is the source of truth for all calculations.
 * This file only formats and displays the returned data.
 */

(function () {
    "use strict";

    const MODULE_NAME = "AIJyotishDasha";

    const DASHA_ORDER = [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury"
    ];

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

    function getValue(object, keys, fallback = null) {
        if (!object || typeof object !== "object") {
            return fallback;
        }

        for (const key of keys) {
            if (
                Object.prototype.hasOwnProperty.call(object, key) &&
                object[key] !== null &&
                object[key] !== undefined
            ) {
                return object[key];
            }
        }

        return fallback;
    }

    function normalizePlanet(value) {
        if (!value) {
            return "";
        }

        const text = String(value).trim();

        const found = DASHA_ORDER.find(
            planet => planet.toLowerCase() === text.toLowerCase()
        );

        return found || text;
    }

    function getSymbol(planet) {
        return PLANET_SYMBOLS[normalizePlanet(planet)] || "✦";
    }

    function getPlanetClass(planet) {
        return PLANET_CLASSES[normalizePlanet(planet)] || "";
    }

    function formatDate(value) {
        if (!value) {
            return "—";
        }

        const date = new Date(value);

        if (Number.isNaN(date.getTime())) {
            return String(value);
        }

        return date.toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });
    }

    function formatDateTime(value) {
        if (!value) {
            return "—";
        }

        const date = new Date(value);

        if (Number.isNaN(date.getTime())) {
            return String(value);
        }

        return date.toLocaleString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        });
    }

    function formatDuration(days) {
        if (days === null || days === undefined || days === "") {
            return "—";
        }

        const number = Number(days);

        if (!Number.isFinite(number)) {
            return String(days);
        }

        const years = Math.floor(number / 365.2425);
        const remainingDays = Math.floor(number % 365.2425);
        const months = Math.floor(remainingDays / 30.44);
        const finalDays = Math.max(
            0,
            Math.round(remainingDays - months * 30.44)
        );

        const parts = [];

        if (years > 0) {
            parts.push(`${years}y`);
        }

        if (months > 0) {
            parts.push(`${months}m`);
        }

        if (finalDays > 0 || parts.length === 0) {
            parts.push(`${finalDays}y`);
        }

        return parts.join(" ");
    }
    function formatRemainingDuration(endDateValue) {
    if (!endDateValue) {
        return "—";
    }

    const endDate = new Date(endDateValue);
    const today = new Date();

    if (Number.isNaN(endDate.getTime())) {
        return "—";
    }

    // Remove time so we calculate calendar days cleanly
    today.setHours(0, 0, 0, 0);
    endDate.setHours(0, 0, 0, 0);

    if (endDate <= today) {
        return "Completed";
    }

    let years = endDate.getFullYear() - today.getFullYear();
    let months = endDate.getMonth() - today.getMonth();
    let days = endDate.getDate() - today.getDate();

    // Borrow days from previous month
    if (days < 0) {
        months--;

        const previousMonth =
            new Date(
                endDate.getFullYear(),
                endDate.getMonth(),
                0
            );

        days += previousMonth.getDate();
    }

    // Borrow months from years
    if (months < 0) {
        years--;
        months += 12;
    }

    const parts = [];

    if (years > 0) {
        parts.push(
            `${years} ${years === 1 ? "Year" : "Years"}`
        );
    }

    if (months > 0) {
        parts.push(
            `${months} ${months === 1 ? "Month" : "Months"}`
        );
    }

    if (days > 0) {
        parts.push(
            `${days} ${days === 1 ? "Day" : "Days"}`
        );
    }

    return parts.length > 0
        ? parts.join(" ")
        : "Less than 1 Day";
}

    function calculateProgress(start, end, now = new Date()) {
        if (!start || !end) {
            return 0;
        }

        const startDate = new Date(start);
        const endDate = new Date(end);
        const currentDate = new Date(now);

        if (
            Number.isNaN(startDate.getTime()) ||
            Number.isNaN(endDate.getTime())
        ) {
            return 0;
        }

        const total = endDate.getTime() - startDate.getTime();
        const elapsed = currentDate.getTime() - startDate.getTime();

        if (total <= 0) {
            return 0;
        }

        return Math.min(100, Math.max(0, (elapsed / total) * 100));
    }

    function isCurrentPeriod(item) {
        if (!item || typeof item !== "object") {
            return false;
        }

        if (
            item.current === true ||
            item.is_current === true ||
            item.active === true
        ) {
            return true;
        }

        const now = new Date();

        const start = getValue(item, [
            "start",
            "start_date",
            "startDate",
            "from",
            "date_from"
        ]);

        const end = getValue(item, [
            "end",
            "end_date",
            "endDate",
            "to",
            "date_to"
        ]);

        if (!start || !end) {
            return false;
        }

        const startDate = new Date(start);
        const endDate = new Date(end);

        if (
            Number.isNaN(startDate.getTime()) ||
            Number.isNaN(endDate.getTime())
        ) {
            return false;
        }

        return now >= startDate && now <= endDate;
    }

    function normalizePeriod(item) {
        if (!item) {
            return null;
        }

        if (typeof item === "string") {
            return {
                planet: normalizePlanet(item),
                start: null,
                end: null,
                current: false,
                duration: null
            };
        }

        const planet = normalizePlanet(
            getValue(item, [
                "planet",
                "lord",
                "dasha_lord",
                "dashaLord",
                "name",
                "major_lord"
            ])
        );

        const start = getValue(item, [
            "start",
            "start_date",
            "startDate",
            "from",
            "date_from"
        ]);

        const end = getValue(item, [
            "end",
            "end_date",
            "endDate",
            "to",
            "date_to"
        ]);

        const duration = getValue(item, [
            "duration",
            "duration_days",
            "days",
            "length"
        ]);

        return {
            ...item,
            planet,
            start,
            end,
            duration,
            current: isCurrentPeriod(item)
        };
    }

    function extractDashaData(chart) {
    const raw =
        chart?.dashas ||
        chart?.dasha ||
        chart?.vimshottari_dasha ||
        chart?.vimshottariDasha ||
        {};

    /*
     * Backend format:
     *
     * dashas: {
     *     system,
     *     nakshatra: {
     *         name,
     *         lord
     *     },
     *     starting_lord,
     *     balance_years,
     *     current_mahadasha,
     *     current_mahadasha_lord,
     *     current_antardasha,
     *     current_antardasha_lord,
     *     mahadasha_timeline,
     *     antardashas
     * }
     */

    if (!raw || typeof raw !== "object") {
        return {
            periods: [],
            current: null,
            antardasha: null,
            birthLord: null,
            status: "Dasha information is not available."
        };
    }

    /* =====================================================
       MAHADASHA TIMELINE
       ===================================================== */

    const timelineRaw =
        raw.mahadasha_timeline ||
        raw.mahadasha ||
        raw.timeline ||
        raw.periods ||
        [];

    const periods = Array.isArray(timelineRaw)
        ? timelineRaw.map(item => {

            const planet = normalizePlanet(
                item?.lord ||
                item?.planet ||
                item?.dasha_lord ||
                item?.name ||
                ""
            );

            const start =
                item?.start_datetime ||
                item?.start ||
                item?.start_date ||
                null;

            const end =
                item?.end_datetime ||
                item?.end ||
                item?.end_date ||
                null;

            return {
                ...item,

                planet,

                start,

                end,

                duration:
                    item?.duration_days ??
                    item?.duration ??
                    item?.duration_years ??
                    null,

                current: false
            };
        }).filter(item => item.planet)
        : [];

    /* =====================================================
       CURRENT MAHADASHA
       ===================================================== */

    let current = null;

    if (
        raw.current_mahadasha &&
        typeof raw.current_mahadasha === "object"
    ) {
        current = normalizePeriod({
            ...raw.current_mahadasha,

            planet:
                raw.current_mahadasha.lord ||
                raw.current_mahadasha.planet
        });
    }

    /*
     * Backend also gives:
     *
     * current_mahadasha_lord: "..."
     *
     * Use that if the complete object is unavailable.
     */

    if (!current && raw.current_mahadasha_lord) {

        const lord = normalizePlanet(
            raw.current_mahadasha_lord
        );

        current =
            periods.find(
                period =>
                    normalizePlanet(period.planet) === lord
            ) || {
                planet: lord,
                start: null,
                end: null,
                duration: null,
                current: true
            };
    }

    /*
     * Final fallback:
     * find a period marked current.
     */

    if (!current) {
        current =
            periods.find(
                period => period.current
            ) || null;
    }

    if (current) {
        current.current = true;
    }

    /* =====================================================
       CURRENT ANTARDASHA
       ===================================================== */

    let antardasha = null;

    if (
        raw.current_antardasha &&
        typeof raw.current_antardasha === "object"
    ) {
        antardasha = normalizePeriod({
            ...raw.current_antardasha,

            planet:
                raw.current_antardasha.lord ||
                raw.current_antardasha.planet
        });
    }

    if (
        !antardasha &&
        raw.current_antardasha_lord
    ) {

        antardasha = {
            planet: normalizePlanet(
                raw.current_antardasha_lord
            ),

            start: null,

            end: null,

            duration: null,

            current: true
        };
    }

    /* =====================================================
       BIRTH NAKSHATRA LORD
       ===================================================== */

    const birthLord = normalizePlanet(
        raw?.nakshatra?.lord ||
        raw?.birth_lord ||
        raw?.birthLord ||
        raw?.nakshatra_lord ||
        raw?.nakshatraLord ||
        chart?.birth_nakshatra_lord ||
        chart?.birthNakshatraLord ||
        ""
    );

    /* =====================================================
       STATUS
       ===================================================== */

    const status =
        raw?.status ||
        raw?.message ||
        null;

    return {
        periods,

        current,

        antardasha,

        birthLord,

        status
    };
}

        

    function findCurrentPeriod(periods) {
        if (!Array.isArray(periods)) {
            return null;
        }

        return periods.find(period => period.current) || null;
    }

    function renderCurrentDasha(data, chart) {
        const container = document.getElementById("currentDasha");

        if (!container) {
            return;
        }

        const current =
            data.current ||
            findCurrentPeriod(data.periods) ||
            null;

        if (!current) {
            container.innerHTML = `
                <div class="dasha-current-empty">
                    <div class="dasha-empty-icon">☾</div>
                    <div>
                        <strong>Current Dasha</strong>
                        <p>Dasha period information is not available.</p>
                    </div>
                </div>
            `;
            return;
        }

        const planet = current.planet || "Unknown";
        const progress = calculateProgress(
            current.start,
            current.end
        );
const duration = formatRemainingDuration(
    current.end
);


        container.innerHTML = `
            <div class="dasha-current-card">
                <div class="dasha-current-header">
                    <div class="dasha-current-planet">
                        <div class="planet-symbol ${getPlanetClass(planet)}">
                            ${escapeHtml(getSymbol(planet))}
                        </div>

                        <div>
                            <span class="dasha-eyebrow">
                                Current Mahadasha
                            </span>

                            <h3>${escapeHtml(planet)}</h3>
                        </div>
                    </div>

                    <span class="dasha-active-badge">
                        <span class="dasha-live-dot"></span>
                        Active
                    </span>
                </div>

                <div class="dasha-current-dates">
                    <div>
                        <span>Started</span>
                        <strong>${escapeHtml(
                            formatDate(current.start)
                        )}</strong>
                    </div>

                    <div>
                        <span>Ends</span>
                        <strong>${escapeHtml(
                            formatDate(current.end)
                        )}</strong>
                    </div>

                    <div>
                        <span>Duration</span>
                        <strong>${escapeHtml(duration)}</strong>
                    </div>
                </div>

                <div class="dasha-progress-wrap">
                    <div class="dasha-progress-label">
                        <span>Period Progress</span>
                        <strong>${progress.toFixed(0)}%</strong>
                    </div>

                    <div class="dasha-progress-track">
                        <div
                            class="dasha-progress-bar"
                            style="width:${progress.toFixed(2)}%"
                        ></div>
                    </div>
                </div>
            </div>
        `;
    }

    function renderDashaDates(data) {
        const container = document.getElementById("dashaDates");

        if (!container) {
            return;
        }

        const current = data.current;

        if (!current) {
            container.innerHTML = "";
            return;
        }

        container.innerHTML = `
            <div class="dasha-date-grid">
                <div class="dasha-date-item">
                    <span class="label">Current Mahadasha</span>
                    <strong>
                        ${escapeHtml(current.planet || "—")}
                    </strong>
                </div>

                <div class="dasha-date-item">
                    <span class="label">Start Date</span>
                    <strong>
                        ${escapeHtml(formatDate(current.start))}
                    </strong>
                </div>

                <div class="dasha-date-item">
                    <span class="label">End Date</span>
                    <strong>
                        ${escapeHtml(formatDate(current.end))}
                    </strong>
                </div>
            </div>
        `;
    }

    function renderBirthLord(data, chart) {
        const container = document.getElementById("dashaBirthLord");

        if (!container) {
            return;
        }

        const lord =
            data.birthLord ||
            chart?.birth_nakshatra_lord ||
            chart?.birthNakshatraLord ||
            "—";

        container.innerHTML = `
            <div class="dasha-birth-lord">
                <div class="dasha-birth-lord-icon ${getPlanetClass(lord)}">
                    ${escapeHtml(getSymbol(lord))}
                </div>

                <div>
                    <span class="label">Birth Nakshatra Lord</span>
                    <strong>${escapeHtml(lord)}</strong>
                </div>
            </div>
        `;
    }

    function renderStatus(data) {
        const container = document.getElementById("dashaStatus");

        if (!container) {
            return;
        }

        if (!data.status) {
            container.innerHTML = "";
            return;
        }

        container.innerHTML = `
            <div class="dasha-status-message">
                <span class="dasha-status-icon">✦</span>
                <span>${escapeHtml(data.status)}</span>
            </div>
        `;
    }

    function renderTimeline(data) {
        const container = document.getElementById("dashaList");

        if (!container) {
            return;
        }

        const periods = data.periods || [];

        if (!periods.length) {
            container.innerHTML = `
                <div class="dasha-empty">
                    <div class="dasha-empty-icon">✦</div>
                    <h3>No Dasha Timeline Available</h3>
                    <p>
                        The calculated Vimshottari Dasha periods
                        are not available in this chart.
                    </p>
                </div>
            `;
            return;
        }

        const current =
            data.current ||
            periods.find(period => period.current) ||
            null;

        container.innerHTML = `
            <div class="dasha-timeline">
                ${periods.map((period, index) => {
                    const planet = period.planet || "Unknown";
                    const active =
                        current &&
                        current.planet === period.planet &&
                        (
                            period.current ||
                            (
                                current.start &&
                                period.start === current.start
                            )
                        );

                    const progress = active
                        ? calculateProgress(
                            period.start,
                            period.end
                        )
                        : 0;

                    return `
                        <article
                            class="dasha-period ${
                                active ? "is-current" : ""
                            }"
                            data-planet="${escapeHtml(planet)}"
                        >
                            <div class="dasha-period-marker">
                                <div
                                    class="dasha-period-symbol ${getPlanetClass(
                                        planet
                                    )}"
                                >
                                    ${escapeHtml(getSymbol(planet))}
                                </div>

                                ${
                                    index < periods.length - 1
                                        ? `<span class="dasha-timeline-line"></span>`
                                        : ""
                                }
                            </div>

                            <div class="dasha-period-content">
                                <div class="dasha-period-top">
                                    <div>
                                        <span class="dasha-period-label">
                                            ${
                                                active
                                                    ? "Current Mahadasha"
                                                    : `Mahadasha ${index + 1}`
                                            }
                                        </span>

                                        <h3>
                                            ${escapeHtml(planet)}
                                        </h3>
                                    </div>

                                    ${
                                        active
                                            ? `
                                                <span class="dasha-active-badge">
                                                    <span class="dasha-live-dot"></span>
                                                    Active
                                                </span>
                                            `
                                            : ""
                                    }
                                </div>

                                <div class="dasha-period-meta">
                                    <div>
                                        <span>From</span>
                                        <strong>
                                            ${escapeHtml(
                                                formatDate(period.start)
                                            )}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>To</span>
                                        <strong>
                                            ${escapeHtml(
                                                formatDate(period.end)
                                            )}
                                        </strong>
                                    </div>

                                    ${
                                        period.duration !== null &&
                                        period.duration !== undefined
                                            ? `
                                                <div>
                                                    <span>Duration</span>
                                                    <strong>
                                                        ${escapeHtml(
                                                            formatDuration(
                                                                period.duration
                                                            )
                                                        )}
                                                    </strong>
                                                </div>
                                            `
                                            : ""
                                    }
                                </div>

                                ${
                                    active
                                        ? `
                                            <div class="dasha-mini-progress">
                                                <div
                                                    class="dasha-mini-progress-bar"
                                                    style="width:${progress.toFixed(
                                                        2
                                                    )}%"
                                                ></div>
                                            </div>
                                        `
                                        : ""
                                }
                            </div>
                        </article>
                    `;
                }).join("")}
            </div>
        `;
    }

    function renderCompactDasha(chart, target) {
        if (!target) {
            return;
        }

        const data = extractDashaData(chart);

        const current =
            data.current ||
            findCurrentPeriod(data.periods);

        if (!current) {
            target.innerHTML = `
                <div class="dasha-compact-empty">
                    Dasha information unavailable
                </div>
            `;
            return;
        }

        target.innerHTML = `
            <div class="dasha-compact">
                <div class="dasha-compact-symbol ${getPlanetClass(
                    current.planet
                )}">
                    ${escapeHtml(getSymbol(current.planet))}
                </div>

                <div class="dasha-compact-content">
                    <span>Current Mahadasha</span>
                    <strong>${escapeHtml(current.planet)}</strong>
                </div>

                <div class="dasha-compact-date">
                    ${escapeHtml(formatDate(current.end))}
                </div>
            </div>
        `;
    }

    function render(chart) {
        if (!chart) {
            return;
        }

        const data = extractDashaData(chart);

        renderCurrentDasha(data, chart);
        renderDashaDates(data);
        renderBirthLord(data, chart);
        renderStatus(data);
        renderTimeline(data);
    }

    function getCurrent(chart) {
        const data = extractDashaData(chart);

        return (
            data.current ||
            findCurrentPeriod(data.periods) ||
            null
        );
    }

    function getTimeline(chart) {
        return extractDashaData(chart).periods || [];
    }

    window[MODULE_NAME] = {
        render,
        renderCurrentDasha,
        renderDashaDates,
        renderBirthLord,
        renderStatus,
        renderTimeline,
        renderCompactDasha,
        extractDashaData,
        getCurrent,
        getTimeline,
        formatDate,
        formatDateTime,
        formatDuration
    };
})();