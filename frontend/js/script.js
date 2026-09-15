/**
 * AI Jyotish — Main Application Controller
 * --------------------------------
 * Connects the frontend modules with the existing backend API.
 *
 * Backend/API routes are intentionally unchanged.
 */

(function () {
    "use strict";

    const APP = window.AIJyotishApp = {};

    let currentChart = null;

    const $ = id => document.getElementById(id);

    function escapeHtml(value) {
        if (value === null || value === undefined) return "";

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function getValue(object, keys, fallback = "—") {
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

    function setText(id, value) {
        const element = $(id);

        if (!element) return;

        element.textContent =
            value === undefined ||
            value === null ||
            value === ""
                ? "—"
                : value;
    }

    function showMessage(id, message, type = "info") {
        const element = $(id);

        if (!element) return;

        element.textContent = message;
        element.className =
            `form-message ${type}`;

        element.hidden = !message;
    }

    function setLoading(button, loading, loadingText = "Loading...") {
        if (!button) return;

        if (loading) {
            button.dataset.originalText =
                button.textContent;

            button.disabled = true;
            button.classList.add("is-loading");
            button.textContent = loadingText;
        } else {
            button.disabled = false;
            button.classList.remove("is-loading");

            if (button.dataset.originalText) {
                button.textContent =
                    button.dataset.originalText;
            }
        }
    }

    function redirect(path) {
        window.location.href = path;
    }

    /* ---------------------------------------------------------
       API
    --------------------------------------------------------- */

    async function apiCall(path, options = {}) {
        if (
            window.AIJyotishAPI &&
            typeof window.AIJyotishAPI.request === "function"
        ) {
            return window.AIJyotishAPI.request(
                path,
                options
            );
        }

        const response = await fetch(path, {
            credentials: "include",
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {})
            }
        });

        let data = {};

        try {
            data = await response.json();
        } catch {
            data = {};
        }

        if (!response.ok) {
            throw new Error(
                data.error ||
                data.message ||
                "Request failed."
            );
        }

        return data;
    }

    async function getCurrentUser() {
        if (
            window.AIJyotishAPI &&
            typeof window.AIJyotishAPI.getCurrentUser === "function"
        ) {
            return window.AIJyotishAPI.getCurrentUser();
        }

        return apiCall("/me");
    }

    async function getLatestKundli() {
        if (
            window.AIJyotishAPI &&
            typeof window.AIJyotishAPI.getLatestKundli === "function"
        ) {
            return window.AIJyotishAPI.getLatestKundli();
        }

        return apiCall("/kundli/latest");
    }

    /* ---------------------------------------------------------
       AUTH
    --------------------------------------------------------- */

    function initLogin() {
        const form = $("loginForm");

        if (!form) return;

        form.addEventListener("submit", async event => {
            event.preventDefault();

            const button =
                form.querySelector(
                    'button[type="submit"]'
                );

            const email =
                $("email")?.value.trim();

            const password =
                $("password")?.value || "";

            if (!email || !password) {
                showMessage(
                    "loginMessage",
                    "Please enter your email and password.",
                    "error"
                );
                return;
            }

            setLoading(
                button,
                true,
                "Signing in..."
            );

            try {
                if (
                    window.AIJyotishAPI &&
                    typeof window.AIJyotishAPI.loginUser === "function"
                ) {
                    await window.AIJyotishAPI.loginUser(
                        email,
                        password
                    );
                } else {
                    await apiCall(
                        "/login",
                        {
                            method: "POST",
                            body: JSON.stringify({
                                email,
                                password
                            })
                        }
                    );
                }

                showMessage(
                    "loginMessage",
                    "Login successful. Opening your dashboard...",
                    "success"
                );

                setTimeout(
                    () => redirect("dashboard.html"),
                    400
                );
            } catch (error) {
                showMessage(
                    "loginMessage",
                    error.message ||
                        "Unable to login.",
                    "error"
                );
            } finally {
                setLoading(button, false);
            }
        });
    }

    function initRegister() {
        const form = $("registerForm");

        if (!form) return;

        form.addEventListener("submit", async event => {
            event.preventDefault();

            const button =
                form.querySelector(
                    'button[type="submit"]'
                );

            const name =
                $("name")?.value.trim();

            const email =
                $("email")?.value.trim();

            const password =
                $("password")?.value || "";

            const confirm =
                $("confirm")?.value || "";

            if (!name || !email || !password) {
                showMessage(
                    "registerMessage",
                    "Please complete all required fields.",
                    "error"
                );
                return;
            }

            if (password !== confirm) {
                showMessage(
                    "registerMessage",
                    "Passwords do not match.",
                    "error"
                );
                return;
            }

            setLoading(
                button,
                true,
                "Creating account..."
            );

            try {
                if (
                    window.AIJyotishAPI &&
                    typeof window.AIJyotishAPI.registerUser === "function"
                ) {
                    await window.AIJyotishAPI.registerUser(
                        name,
                        email,
                        password
                    );
                } else {
                    await apiCall(
                        "/register",
                        {
                            method: "POST",
                            body: JSON.stringify({
                                name,
                                email,
                                password,
                                confirm
                            })
                        }
                    );
                }

                showMessage(
                    "registerMessage",
                    "Account created successfully. You can now login.",
                    "success"
                );

                form.reset();

                setTimeout(
                    () => redirect("login.html"),
                    800
                );
            } catch (error) {
                showMessage(
                    "registerMessage",
                    error.message ||
                        "Unable to create account.",
                    "error"
                );
            } finally {
                setLoading(button, false);
            }
        });
    }

    async function logout() {
        try {
            if (
                window.AIJyotishAPI &&
                typeof window.AIJyotishAPI.logoutUser === "function"
            ) {
                await window.AIJyotishAPI.logoutUser();
            } else {
                await apiCall(
                    "/logout",
                    {
                        method: "POST"
                    }
                );
            }
        } catch {
            // Continue redirecting even if the logout request fails.
        }

        redirect("login.html");
    }

    function initLogout() {
        const buttons =
            document.querySelectorAll(
                "#logoutBtn, [data-action='logout']"
            );

        buttons.forEach(button => {
            button.addEventListener(
                "click",
                event => {
                    event.preventDefault();
                    logout();
                }
            );
        });
    }

    /* ---------------------------------------------------------
       BIRTH FORM
    --------------------------------------------------------- */

    function initBirthForm() {
        const form = $("birthForm");

        if (!form) return;
        // ---------------------------------------------------------
// CURRENT LOCATION
// ---------------------------------------------------------

// CURRENT LOCATION + BIRTHPLACE SEARCH
const locationBtn = $("useLocationBtn");
const locationStatus = $("locationStatus");
const placeInput = $("place");


// =====================================================
// FUNCTION: SET LOCATION DATA
// =====================================================
function setLocationData(latitude, longitude, placeName = "") {

    const latitudeInput = $("latitude");
    const longitudeInput = $("longitude");
    const timezoneInput = $("timezone");

    if (latitudeInput) {
        latitudeInput.value = Number(latitude).toFixed(6);
    }

    if (longitudeInput) {
        longitudeInput.value = Number(longitude).toFixed(6);
    }

    // Browser local timezone
    const timezoneOffset =
        -new Date().getTimezoneOffset() / 60;

    if (timezoneInput) {
        timezoneInput.value = timezoneOffset;
    }

    if (placeInput && placeName) {
        placeInput.value = placeName;
    }
}


// =====================================================
// USE CURRENT GPS LOCATION
// =====================================================
if (locationBtn) {

    locationBtn.addEventListener("click", () => {

        if (!navigator.geolocation) {

            if (locationStatus) {
                locationStatus.textContent =
                    "Location access is not supported by your browser.";
            }

            return;
        }

        locationBtn.disabled = true;

        locationBtn.textContent =
            "📍 Detecting location...";

        if (locationStatus) {
            locationStatus.textContent =
                "Please allow location access when your browser asks.";
        }


        navigator.geolocation.getCurrentPosition(

            async position => {

                const latitude =
                    position.coords.latitude;

                const longitude =
                    position.coords.longitude;


                setLocationData(
                    latitude,
                    longitude
                );


                if (locationStatus) {
                    locationStatus.textContent =
                        "📍 Finding place name...";
                }


                try {

                    const url =
                        "https://nominatim.openstreetmap.org/reverse" +
                        "?format=jsonv2" +
                        "&lat=" +
                        encodeURIComponent(latitude) +
                        "&lon=" +
                        encodeURIComponent(longitude) +
                        "&addressdetails=1" +
                        "&zoom=10" +
                        "&accept-language=en";


                    const response =
                        await fetch(url);


                    if (!response.ok) {
                        throw new Error(
                            "Reverse geocoding failed"
                        );
                    }


                    const data =
                        await response.json();

                    const address =
                        data?.address || {};


                    const city =
                        address.city ||
                        address.town ||
                        address.village ||
                        address.municipality ||
                        address.county ||
                        "";


                    const state =
                        address.state ||
                        address.state_district ||
                        "";


                    const country =
                        address.country ||
                        "";


                    const birthplace =
                        [
                            city,
                            state,
                            country
                        ]
                        .filter(Boolean)
                        .join(", ");


                    if (
                        placeInput &&
                        birthplace
                    ) {
                        placeInput.value =
                            birthplace;
                    }


                    locationBtn.disabled = false;

                    locationBtn.textContent =
                        "✓ Location detected";


                    if (locationStatus) {

                        locationStatus.textContent =
                            birthplace
                                ? `✓ ${birthplace} — edit if this is not your birthplace`
                                : "✓ Location detected. Please enter your birthplace.";
                    }


                } catch (error) {

                    console.error(
                        "Reverse geocoding error:",
                        error
                    );


                    locationBtn.disabled = false;

                    locationBtn.textContent =
                        "✓ Coordinates detected";


                    if (locationStatus) {

                        locationStatus.textContent =
                            "Coordinates detected. Please enter your birthplace manually.";
                    }
                }
            },


            error => {

                locationBtn.disabled = false;

                locationBtn.textContent =
                    "📍 Use my current location";


                if (!locationStatus) return;


                if (error.code === 1) {

                    locationStatus.textContent =
                        "Location permission was denied. Please allow it and try again.";

                } else if (error.code === 2) {

                    locationStatus.textContent =
                        "Your location could not be determined. Please try again.";

                } else if (error.code === 3) {

                    locationStatus.textContent =
                        "Location request timed out. Please try again.";

                } else {

                    locationStatus.textContent =
                        "Unable to detect your location.";
                }
            },


            {
                enableHighAccuracy: true,
                timeout: 15000,
                maximumAge: 300000
            }
        );
    });
}


// =====================================================
// BIRTHPLACE SEARCH
// User types a place and selects the correct result.
// Latitude + Longitude are automatically filled.
// =====================================================

if (placeInput) {

    // Create suggestion box
    const suggestionBox =
        document.createElement("div");

    suggestionBox.id =
        "birthplaceSuggestions";

    suggestionBox.style.position =
        "absolute";

    suggestionBox.style.zIndex =
        "9999";

    suggestionBox.style.background =
        "#ffffff";

    suggestionBox.style.border =
        "1px solid #ddd";

    suggestionBox.style.borderRadius =
        "8px";

    suggestionBox.style.boxShadow =
        "0 4px 12px rgba(0,0,0,0.12)";

    suggestionBox.style.width =
        "100%";

    suggestionBox.style.maxHeight =
        "250px";

    suggestionBox.style.overflowY =
        "auto";

    suggestionBox.style.display =
        "none";


    // Make parent relative
    const placeParent =
        placeInput.parentElement;

    if (placeParent) {

        placeParent.style.position =
            "relative";

        placeParent.appendChild(
            suggestionBox
        );
    }


    let searchTimer = null;


    placeInput.addEventListener(
        "input",
        () => {

            const query =
                placeInput.value.trim();


            clearTimeout(searchTimer);


            if (query.length < 2) {

                suggestionBox.innerHTML =
                    "";

                suggestionBox.style.display =
                    "none";

                return;
            }


            searchTimer =
                setTimeout(
                    async () => {

                        try {

                            suggestionBox.innerHTML =
                                "<div style='padding:10px;color:#777;'>Searching...</div>";

                            suggestionBox.style.display =
                                "block";


                            const url =
                                "https://nominatim.openstreetmap.org/search" +
                                "?format=jsonv2" +
                                "&q=" +
                                encodeURIComponent(query) +
                                "&addressdetails=1" +
                                "&limit=5" +
                                "&accept-language=en";


                            const response =
                                await fetch(url);


                            if (!response.ok) {
                                throw new Error(
                                    "Place search failed"
                                );
                            }


                            const results =
                                await response.json();


                            suggestionBox.innerHTML =
                                "";


                            if (
                                !results ||
                                results.length === 0
                            ) {

                                suggestionBox.innerHTML =
                                    "<div style='padding:10px;color:#777;'>No location found</div>";

                                return;
                            }


                          results.forEach(result => {

    const item =
        document.createElement("div");

    item.style.padding =
        "12px 14px";

    item.style.cursor =
        "pointer";

    item.style.borderBottom =
        "1px solid #eeeeee";

    item.style.fontSize =
        "14px";

    // FIX: suggestion text color
    item.style.color =
        "#111827";

    item.style.backgroundColor =
        "#ffffff";

    item.style.fontWeight =
        "500";

    item.style.lineHeight =
        "1.4";

    item.textContent =
        result.display_name;


    item.addEventListener(
        "mouseenter",
        () => {
            item.style.backgroundColor =
                "#f3f4f6";
        }
    );


    item.addEventListener(
        "mouseleave",
        () => {
            item.style.backgroundColor =
                "#ffffff";
        }
    );


    item.addEventListener(
        "click",
        () => {

            const latitude =
                parseFloat(result.lat);

            const longitude =
                parseFloat(result.lon);

            const address =
                result.address || {};

            const city =
                address.city ||
                address.town ||
                address.village ||
                address.municipality ||
                address.county ||
                "";

            const state =
                address.state ||
                address.state_district ||
                "";

            const country =
                address.country ||
                "";

            const birthplace =
                [
                    city,
                    state,
                    country
                ]
                .filter(Boolean)
                .join(", ");


            setLocationData(
                latitude,
                longitude,
                birthplace ||
                result.display_name
            );


            suggestionBox.innerHTML =
                "";

            suggestionBox.style.display =
                "none";


            if (locationStatus) {
                locationStatus.textContent =
                    `✓ Birthplace selected: ${birthplace || result.display_name}`;
            }
        }
    );


    suggestionBox.appendChild(item);
});


                        } catch (error) {

                            console.error(
                                "Birthplace search error:",
                                error
                            );


                            suggestionBox.innerHTML =
                                "<div style='padding:10px;color:#b00;'>Unable to search location. Please try again.</div>";

                            suggestionBox.style.display =
                                "block";
                        }

                    },
                    500
                );
        }
    );


    // Hide suggestions when clicking outside
    document.addEventListener(
        "click",
        event => {

            if (
                event.target !== placeInput &&
                !suggestionBox.contains(
                    event.target
                )
            ) {

                suggestionBox.style.display =
                    "none";
            }
        }
    );
}

        form.addEventListener("submit", async event => {
            event.preventDefault();

            const button = $("generateBtn");

            const name =
                $("name")?.value.trim();

            const date =
                $("date")?.value;

            const time =
                ($("time")?.value || "").slice(0, 5);

            const place =
                $("place")?.value.trim();

            const latitude =
                $("latitude")?.value;

            const longitude =
                $("longitude")?.value;

            const timezone =
                $("timezone")?.value;

            if (
                !name ||
                !date ||
                !time ||
                !place ||
                latitude === "" ||
                longitude === "" ||
                timezone === ""
            ) {
                showMessage(
                    "birthMessage",
                    "Please complete all birth details.",
                    "error"
                );
                return;
            }

            setLoading(
                button,
                true,
                "Calculating Kundli..."
            );

            try {
                const body = {
                    name,
                    date,
                    time,
                    place,
                    latitude: Number(latitude),
                    longitude: Number(longitude),
                    timezone: Number(timezone)
                };

                let result;

                if (
                    window.AIJyotishAPI &&
                    typeof window.AIJyotishAPI.generateKundli === "function"
                ) {
                    result =
                        await window.AIJyotishAPI.generateKundli(
                            body
                        );
                } else {
                    result =
                        await apiCall(
                            "/kundli",
                            {
                                method: "POST",
                                body: JSON.stringify(body)
                            }
                        );
                }

           currentChart =
    result?.chart ||
    result?.kundli ||
    result?.data ||
    result;

sessionStorage.setItem(
    "aiJyotishKundliName",
    name
);

sessionStorage.setItem(
    "aiJyotishLatestChart",
    JSON.stringify(currentChart)
);

showMessage(
    "Kundli generated successfully!",
    "success"
);

setTimeout(() => {
    redirect("kundli.html");
}, 500);
/* =================================================
   SAVE THE NAME OF THE PERSON WHOSE KUNDLI
   WAS JUST CREATED
   ================================================= */

sessionStorage.setItem(
    "aiJyotishKundliName",
    name
);


/* =================================================
   SAVE COMPLETE CHART
   ================================================= */

sessionStorage.setItem(
    "aiJyotishLatestChart",
    JSON.stringify(
        currentChart
    )
);

                showMessage(
                    "birthMessage",
                    "Kundli calculated successfully.",
                    "success"
                );

                setTimeout(
                    () => redirect("kundli.html"),
                    500
                );
            } catch (error) {
                showMessage(
                    "birthMessage",
                    error.message ||
                        "Unable to calculate Kundli.",
                    "error"
                );
            } finally {
                setLoading(
                    button,
                    false
                );
            }
        });
    }

    /* ---------------------------------------------------------
       KUNDLI RENDERING
    --------------------------------------------------------- */

    function getPlanetArray(chart) {
        const source =
            chart?.planets ||
            chart?.planetary_positions ||
            chart?.planetaryPositions ||
            [];

        if (Array.isArray(source)) {
            return source;
        }

        if (
            source &&
            typeof source === "object"
        ) {
            return Object.entries(source)
                .map(([name, data]) => ({
                    ...(data || {}),
                    name:
                        data?.name ||
                        data?.planet ||
                        name
                }));
        }

        return [];
    }

    function renderHeader(chart) {
        const name = getValue(
            chart,
            ["name", "full_name", "fullName"],
            "Birth Chart"
        );

        const date = getValue(
            chart,
            ["birth_date", "birthDate", "date"],
            "—"
        );

        const time = getValue(
            chart,
            ["birth_time", "birthTime", "time"],
            "—"
        );

        const place = getValue(
            chart,
            ["place", "birth_place", "birthPlace"],
            "—"
        );

        const ascObject = chart?.ascendant;
        const asc =
            (ascObject && typeof ascObject === "object"
                ? getValue(ascObject, ["sign", "rashi", "name"], "—")
                : ascObject) ||
            getValue(chart, ["ascendant_sign", "ascendantSign", "lagna"], "—");

        const sun = getValue(
            chart,
            ["sun_sign", "sunSign", "sun_rashi"],
            "—"
        );

        const moon = getValue(
            chart,
            ["moon_sign", "moonSign", "moon_rashi"],
            "—"
        );

        const moonPlanet = getPlanetArray(chart).find(
            planet => String(planet?.name || planet?.planet || "").toLowerCase() === "moon"
        ) || {};

        const nakshatra =
            getValue(chart, ["moon_nakshatra", "birth_nakshatra", "birthNakshatra", "nakshatra"], null) ||
            getValue(moonPlanet, ["nakshatra", "star"], "—");

        const lord =
            getValue(chart, ["moon_nakshatra_lord", "birth_nakshatra_lord", "birthNakshatraLord", "nakshatra_lord"], null) ||
            getValue(moonPlanet, ["nakshatra_lord", "nakshatraLord", "star_lord"], "—");

        const pada =
            getValue(chart, ["moon_pada", "birth_pada", "birthPada", "pada"], null) ||
            getValue(moonPlanet, ["pada", "quarter"], "—");

        setText("chartName", name);
        setText("chartBirth", `${date} • ${time}`);
        setText("chartPlace", place);
        setText("chartAsc", asc);
        setText("chartSun", sun);
        setText("chartMoon", moon);
        setText("birthNakshatra", nakshatra);
        setText("birthNakshatraLord", lord);
        setText("birthPada", pada);
    }

    function renderCalculationDetails(chart) {
        const calculation = chart?.calculation || {};

        setText(
            "calcZodiac",
            getValue(calculation, ["zodiac", "zodiac_system", "zodiacSystem"],
                getValue(chart, ["zodiac", "zodiac_system", "zodiacSystem"], "—"))
        );

        setText(
            "calcAyanamsha",
            getValue(calculation, ["ayanamsha", "ayanamsa", "ayanamsha_value"],
                getValue(chart, ["ayanamsha", "ayanamsa", "ayanamsha_value"], "—"))
        );

        setText(
            "calcHouse",
            getValue(calculation, ["house_system", "houseSystem"],
                getValue(chart, ["house_system", "houseSystem"], "—"))
        );

        setText(
            "julianDay",
            getValue(chart, ["julian_day", "julianDay", "jd"], "—")
        );
    }
function renderAscendantDetails(chart) {
    const container = $("ascDetails");

    if (!container) return;

    /*
     * Backend normally provides ascendant data as:
     *
     * chart.ascendant = {
     *     sign: "Kanya",
     *     degree: 8.2751,
     *     longitude: 158.2751
     * }
     *
     * Support both the old and new structures.
     */
    const asc =
        chart?.ascendant_details ||
        chart?.ascendantDetails ||
        chart?.ascendant_info ||
        chart?.ascendant ||
        null;

    if (!asc) {
        container.innerHTML = `
            <div class="asc-details-empty">
                Ascendant information unavailable.
            </div>
        `;
        return;
    }

    /* -----------------------------------------
       BASIC ASCENDANT DATA
    ----------------------------------------- */

    const sign =
        getValue(
            asc,
            ["sign", "rashi", "name"],
            getValue(
                chart,
                [
                    "ascendant_sign",
                    "ascendantSign",
                    "lagna"
                ],
                "—"
            )
        );

    const degree =
        getValue(
            asc,
            [
                "degree",
                "degrees",
                "degree_in_sign"
            ],
            "—"
        );

    const longitude =
        getValue(
            asc,
            [
                "longitude",
                "absolute_longitude",
                "longitude_deg"
            ],
            "—"
        );

    /* -----------------------------------------
       NAKSHATRA
    ----------------------------------------- */

    let nakshatra =
        getValue(
            asc,
            [
                "nakshatra",
                "star"
            ],
            ""
        );

    let nakshatraLord =
        getValue(
            asc,
            [
                "nakshatra_lord",
                "lord"
            ],
            ""
        );

    /*
     * If backend does not directly provide
     * Nakshatra, calculate it from longitude.
     */
    if (
        !nakshatra ||
        nakshatra === "—"
    ) {
        const lon = Number(longitude);

        if (Number.isFinite(lon)) {

            const nakshatras = [
                ["Ashwini", "Ketu"],
                ["Bharani", "Venus"],
                ["Krittika", "Sun"],
                ["Rohini", "Moon"],
                ["Mrigashira", "Mars"],
                ["Ardra", "Rahu"],
                ["Punarvasu", "Jupiter"],
                ["Pushya", "Saturn"],
                ["Ashlesha", "Mercury"],
                ["Magha", "Ketu"],
                ["Purva Phalguni", "Venus"],
                ["Uttara Phalguni", "Sun"],
                ["Hasta", "Moon"],
                ["Chitra", "Mars"],
                ["Swati", "Rahu"],
                ["Vishakha", "Jupiter"],
                ["Anuradha", "Saturn"],
                ["Jyeshtha", "Mercury"],
                ["Mula", "Ketu"],
                ["Purva Ashadha", "Venus"],
                ["Uttara Ashadha", "Sun"],
                ["Shravana", "Moon"],
                ["Dhanishta", "Mars"],
                ["Shatabhisha", "Rahu"],
                ["Purva Bhadrapada", "Jupiter"],
                ["Uttara Bhadrapada", "Saturn"],
                ["Revati", "Mercury"]
            ];

            const normalizedLongitude =
                ((lon % 360) + 360) % 360;

            const nakshatraSize =
                360 / 27;

            const index =
                Math.floor(
                    normalizedLongitude /
                    nakshatraSize
                );

            if (nakshatras[index]) {
                nakshatra =
                    nakshatras[index][0];

                if (
                    !nakshatraLord ||
                    nakshatraLord === "—"
                ) {
                    nakshatraLord =
                        nakshatras[index][1];
                }
            }
        }
    }

    /*
     * -----------------------------------------
       RASHI LORD
    ----------------------------------------- */

    const rashiLords = {
        Aries: "Mars",
        Taurus: "Venus",
        Gemini: "Mercury",
        Cancer: "Moon",
        Leo: "Sun",
        Virgo: "Mercury",
        Libra: "Venus",
        Scorpio: "Mars",
        Sagittarius: "Jupiter",
        Capricorn: "Saturn",
        Aquarius: "Saturn",
        Pisces: "Jupiter",

        Mesha: "Mars",
        Vrishabha: "Venus",
        Mithuna: "Mercury",
        Karka: "Moon",
        Simha: "Sun",
        Kanya: "Mercury",
        Tula: "Venus",
        Vrishchika: "Mars",
        Dhanu: "Jupiter",
        Makara: "Saturn",
        Kumbha: "Saturn",
        Meena: "Jupiter"
    };

    const rashiLord =
        rashiLords[sign] || "—";

    /*
     * -----------------------------------------
       DISPLAY
    ----------------------------------------- */

    container.innerHTML = `
        <div class="asc-details-list">

            <div class="asc-detail-row">
                <span>Ascendant:</span>
                <strong>
                    ${escapeHtml(sign)}
                </strong>
            </div>

            <div class="asc-detail-row">
                <span>Degree:</span>
                <strong>
                    ${escapeHtml(degree)}
                </strong>
            </div>

            <div class="asc-detail-row">
                <span>Longitude:</span>
                <strong>
                    ${escapeHtml(longitude)}
                </strong>
            </div>

            <div class="asc-detail-row">
                <span>Nakshatra:</span>
                <strong>
                    ${escapeHtml(
                        nakshatra || "—"
                    )}
                </strong>
            </div>

            <div class="asc-detail-row">
                <span>Nakshatra Lord:</span>
                <strong>
                    ${escapeHtml(
                        nakshatraLord || "—"
                    )}
                </strong>
            </div>

            <div class="asc-detail-row">
                <span>Rashi Lord:</span>
                <strong>
                    ${escapeHtml(rashiLord)}
                </strong>
            </div>

        </div>
    `;
}
function getPlanetStatus(planet) {
    const name = String(
        getValue(
            planet,
            ["name", "planet", "body"],
            ""
        )
    ).trim();

    const sign = String(
        getValue(
            planet,
            ["sign", "rashi", "zodiac"],
            ""
        )
    ).trim();

    if (!name || !sign) {
        return "—";
    }

    const dignity = {
        Sun: {
            exalted: ["Aries", "Mesha"],
            debilitated: ["Libra", "Tula"],
            own: ["Leo", "Simha"]
        },

        Moon: {
            exalted: ["Taurus", "Vrishabha"],
            debilitated: ["Scorpio", "Vrishchika"],
            own: ["Cancer", "Karka"]
        },

        Mars: {
            exalted: ["Capricorn", "Makara"],
            debilitated: ["Cancer", "Karka"],
            own: ["Aries", "Mesha", "Scorpio", "Vrishchika"]
        },

        Mercury: {
            exalted: ["Virgo", "Kanya"],
            debilitated: ["Pisces", "Meena"],
            own: ["Gemini", "Mithuna", "Virgo", "Kanya"]
        },

        Jupiter: {
            exalted: ["Cancer", "Karka"],
            debilitated: ["Capricorn", "Makara"],
            own: ["Sagittarius", "Dhanu", "Pisces", "Meena"]
        },

        Venus: {
            exalted: ["Pisces", "Meena"],
            debilitated: ["Virgo", "Kanya"],
            own: ["Taurus", "Vrishabha", "Libra", "Tula"]
        },

        Saturn: {
            exalted: ["Libra", "Tula"],
            debilitated: ["Aries", "Mesha"],
            own: ["Capricorn", "Makara", "Aquarius", "Kumbha"]
        }
    };

    const data = dignity[name];

    if (!data) {
        /*
         * Rahu and Ketu have differing traditional
         * dignity systems, so don't make a
         * potentially misleading claim here.
         */
        return "R";
    }

    if (data.exalted.includes(sign)) {
        return "Exalted";
    }

    if (data.debilitated.includes(sign)) {
        return "Debilitated";
    }

    if (data.own.includes(sign)) {
        return "Own Sign";
    }

    return "Normal";
}

    function renderPlanetTable(chart) {
        const tbody =
            $("planetBody");

        if (!tbody) return;

        const planets =
            getPlanetArray(chart);

        if (!planets.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9">
                        No planetary data available.
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML =
            planets.map(planet => {
                const name =
                    getValue(
                        planet,
                        ["name", "planet", "body"],
                        "—"
                    );

                const sign =
                    getValue(
                        planet,
                        ["sign", "rashi", "zodiac"],
                        "—"
                    );

                const degree =
                    getValue(
                        planet,
                        ["degree", "degrees"],
                        "—"
                    );

                const longitude =
                    getValue(
                        planet,
                        [
                            "longitude",
                            "absolute_longitude",
                            "absoluteLongitude"
                        ],
                        "—"
                    );

                const house =
                    getValue(
                        planet,
                        [
                            "house",
                            "house_number",
                            "houseNumber"
                        ],
                        "—"
                    );

                        const nakshatraModule = window.AIJyotishNakshatra;
                const derivedNakshatra =
                    nakshatraModule &&
                    typeof nakshatraModule.getNakshatraData === "function"
                        ? nakshatraModule.getNakshatraData(planet)
                        : null;

                const nakshatra =
                    getValue(
                        planet,
                        ["nakshatra", "star"],
                        derivedNakshatra?.name || "—"
                    );

                const lord =
                    getValue(
                        planet,
                        [
                            "nakshatra_lord",
                            "nakshatraLord",
                            "star_lord"
                        ],
                        derivedNakshatra?.lord || "—"
                    );

                const pada =
                    getValue(
                        planet,
                        ["pada", "quarter"],
                        derivedNakshatra?.pada || "—"
                    );

                const status = getPlanetStatus(planet);

                return `
                    <tr>
                        <td>
                            <strong>
                                ${escapeHtml(name)}
                            </strong>
                        </td>

                        <td>
                            ${escapeHtml(sign)}
                        </td>

                        <td>
                            ${escapeHtml(degree)}
                        </td>

                        <td>
                            ${escapeHtml(longitude)}
                        </td>

                        <td>
                            ${escapeHtml(house)}
                        </td>

                        <td>
                            ${escapeHtml(nakshatra)}
                        </td>

                        <td>
                            ${escapeHtml(lord)}
                        </td>

                        <td>
                            ${escapeHtml(pada)}
                        </td>

                        <td>
                            <span class="planet-status">
                                ${escapeHtml(status)}
                            </span>
                        </td>
                    </tr>
                `;
            }).join("");
    }

    function renderNorthIndianChart(chart) {
        const container =
            $("kundliSvg");

        if (!container) return;

        if (
            window.AIJyotishCharts &&
            typeof window.AIJyotishCharts.renderNorthIndianChart ===
                "function"
        ) {
            window.AIJyotishCharts.renderNorthIndianChart(
                container,
                chart
            );
            return;
        }

        container.innerHTML = `
            <div class="chart-fallback">
                <span>✦</span>
                <p>Birth chart visual unavailable.</p>
            </div>
        `;
    }

    function renderPlanetPositionVisual(chart) {
        /*
         * A separate planetary-position visual.
         *
         * The data comes from the actual calculated
         * longitude/sign values returned by the backend.
         */
        let container =
            $("planetPositionVisual");

        if (!container) {
            const section =
                $("kundliPage") ||
                document.querySelector(
                    ".kundli-page"
                );

            if (!section) return;

            container =
                document.createElement("div");

            container.id =
                "planetPositionVisual";

            container.className =
                "planet-position-visual";

            const anchor =
                $("kundliSvg")?.closest(
                    "section"
                );

            if (anchor) {
                anchor.insertAdjacentElement(
                    "afterend",
                    container
                );
            } else {
                section.appendChild(
                    container
                );
            }
        }

        if (
            window.AIJyotishCharts &&
            typeof window.AIJyotishCharts
                .renderPlanetPositionVisual ===
                "function"
        ) {
            window.AIJyotishCharts
                .renderPlanetPositionVisual(
                    container,
                    chart
                );
        }
    }

    function renderDasha(chart) {
        if (
            window.AIJyotishDasha &&
            typeof window.AIJyotishDasha.render ===
                "function"
        ) {
            window.AIJyotishDasha.render(
                chart
            );
        }
    }

    function renderYogas(chart) {
        if (
            window.AIJyotishYogas &&
            typeof window.AIJyotishYogas.render ===
                "function"
        ) {
            window.AIJyotishYogas.render(
                chart
            );
        }
    }

    function renderDashboard(chart) {
        if (
            window.AIJyotishDashboard &&
            typeof window.AIJyotishDashboard.render ===
                "function"
        ) {
            window.AIJyotishDashboard.render(
                chart
            );
        }
    }

    function renderPlanets(chart) {
        const container = $("planetCards");
        if (!container) return;

        if (
            window.AIJyotishPlanets &&
            typeof window.AIJyotishPlanets.renderPlanetCards === "function"
        ) {
            window.AIJyotishPlanets.renderPlanetCards(
                container,
                chart
            );
            return;
        }

        container.innerHTML = "<div class=\"planet-empty\">Planet analysis unavailable.</div>";
    }

    function renderNakshatra(chart) {
        const planets = getPlanetArray(chart);
        const moon = planets.find(
            planet => String(planet?.name || planet?.planet || "").toLowerCase() === "moon"
        );

        const birth = window.AIJyotishNakshatra;

        let nakshatra =
            getValue(chart, ["moon_nakshatra", "birth_nakshatra"], null) ||
            getValue(moon, ["nakshatra", "star"], null);

        let lord =
            getValue(chart, ["moon_nakshatra_lord", "birth_nakshatra_lord"], null) ||
            getValue(moon, ["nakshatra_lord", "nakshatraLord"], null);

        let pada =
            getValue(chart, ["moon_pada", "birth_pada"], null) ||
            getValue(moon, ["pada", "quarter"], null);

        // Final frontend fallback: derive Nakshatra directly from the
        // already-calculated Moon longitude. This does not recalculate
        // planetary positions; it only labels the existing longitude.
        if ((!nakshatra || !lord || !pada) && birth && moon) {
            const longitude = getValue(moon, ["longitude", "absolute_longitude", "absoluteLongitude"], null);
            if (longitude !== null && typeof birth.getNakshatraData === "function") {
                const data = birth.getNakshatraData(moon);
                if (data) {
                    nakshatra = nakshatra || data.name;
                    lord = lord || data.lord;
                    pada = pada || data.pada;
                }
            }
        }

        setText("birthNakshatra", nakshatra || "—");
        setText("birthNakshatraLord", lord || "—");
        setText("birthPada", pada || "—");
    }

    function renderCompleteAnalysis(chart) {
        if (
            window.AIJyotishKundli &&
            typeof window.AIJyotishKundli
                .renderCompleteAnalysis ===
                "function"
        ) {
            window.AIJyotishKundli
                .renderCompleteAnalysis(
                    chart
                );
        }
    }

    function renderKundli(chart) {
    if (!chart) return;

    currentChart = chart;

    renderHeader(chart);
    renderCalculationDetails(chart);
    renderAscendantDetails(chart);

    // Main Birth Chart
    renderNorthIndianChart(chart);

    // 🌙 Chandra Kundli + ⭐ Navamsha D9
    if (
        window.AIJyotishCharts &&
        typeof window.AIJyotishCharts.renderSpecialCharts === "function"
    ) {
        window.AIJyotishCharts.renderSpecialCharts(chart);
    }

    renderPlanetPositionVisual(chart);
    renderPlanetTable(chart);

    renderPlanets(chart);
    renderNakshatra(chart);
    renderDasha(chart);
    renderYogas(chart);
    renderCompleteAnalysis(chart);
}

    /* ---------------------------------------------------------
       HOUSES
    --------------------------------------------------------- */

   function renderHouses(chart) {
    const container = $("houseGrid");

    if (!container || !chart) return;

    /* ---------------------------------------------
       HOUSE NAMES
    --------------------------------------------- */

    const houseNames = {
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

    /* ---------------------------------------------
       RASHI DATA
    --------------------------------------------- */

    const rashiData = [
        { name: "Mesha", lord: "Mars" },
        { name: "Vrishabha", lord: "Venus" },
        { name: "Mithuna", lord: "Mercury" },
        { name: "Karka", lord: "Moon" },
        { name: "Simha", lord: "Sun" },
        { name: "Kanya", lord: "Mercury" },
        { name: "Tula", lord: "Venus" },
        { name: "Vrishchika", lord: "Mars" },
        { name: "Dhanu", lord: "Jupiter" },
        { name: "Makara", lord: "Saturn" },
        { name: "Kumbha", lord: "Saturn" },
        { name: "Meena", lord: "Jupiter" }
    ];

    const signAliases = {
        mesha: 0,
        aries: 0,

        vrishabha: 1,
        taurus: 1,

        mithuna: 2,
        gemini: 2,

        karka: 3,
        cancer: 3,

        simha: 4,
        leo: 4,

        kanya: 5,
        virgo: 5,

        tula: 6,
        libra: 6,

        vrishchika: 7,
        scorpio: 7,

        dhanu: 8,
        sagittarius: 8,

        makara: 9,
        capricorn: 9,

        kumbha: 10,
        aquarius: 10,

        meena: 11,
        pisces: 11
    };

    /* ---------------------------------------------
       GET ASCENDANT
    --------------------------------------------- */

    const ascendant =
        chart.ascendant ||
        chart.ascendant_sign ||
        chart.ascendantSign ||
        chart.lagna;

    let ascSignIndex = null;

    if (
        ascendant &&
        typeof ascendant === "object"
    ) {
        const rawIndex =
            ascendant.sign_index ??
            ascendant.signIndex ??
            ascendant.rashi_index ??
            ascendant.rashiIndex;

        const numericIndex = Number(rawIndex);

        if (
            Number.isInteger(numericIndex) &&
            numericIndex >= 0 &&
            numericIndex <= 11
        ) {
            ascSignIndex = numericIndex;
        }

        if (ascSignIndex === null) {
            const signText = String(
                ascendant.sign ||
                ascendant.rashi ||
                ascendant.name ||
                ""
            )
                .trim()
                .toLowerCase();

            if (
                signAliases[signText] !== undefined
            ) {
                ascSignIndex =
                    signAliases[signText];
            }
        }
    } else {
        const signText = String(
            ascendant || ""
        )
            .trim()
            .toLowerCase();

        if (
            signAliases[signText] !== undefined
        ) {
            ascSignIndex =
                signAliases[signText];
        }
    }

    /* ---------------------------------------------
       GET ACTUAL PLANETS
    --------------------------------------------- */

    const source =
        chart.planets ||
        chart.planetary_positions ||
        chart.planetaryPositions ||
        [];

    const planets = Array.isArray(source)
        ? source
        : Object.entries(source || {}).map(
            ([name, data]) => ({
                ...(data || {}),
                name:
                    data?.name ||
                    data?.planet ||
                    name
            })
        );

    /* ---------------------------------------------
       CREATE 12 EMPTY HOUSES
    --------------------------------------------- */

    const planetsByHouse = {};

    for (let house = 1; house <= 12; house++) {
        planetsByHouse[house] = [];
    }

    /* ---------------------------------------------
       PUT EVERY PLANET INTO ITS ACTUAL HOUSE
    --------------------------------------------- */

    planets.forEach(planet => {

        let house = Number(
            planet?.house ??
            planet?.house_number ??
            planet?.houseNumber ??
            planet?.bhava
        );

        /*
         * If backend already gives house,
         * use that directly.
         */

        if (
            Number.isInteger(house) &&
            house >= 1 &&
            house <= 12
        ) {
            planetsByHouse[house].push(
                String(
                    planet?.name ||
                    planet?.planet ||
                    planet?.body ||
                    "Planet"
                )
            );

            return;
        }

        /*
         * Fallback:
         * If house is missing but sign is available,
         * calculate whole-sign house from Ascendant.
         */

        if (ascSignIndex !== null) {

            const planetSign =
                String(
                    planet?.sign ||
                    planet?.rashi ||
                    planet?.zodiac ||
                    ""
                )
                    .trim()
                    .toLowerCase();

            const planetSignIndex =
                signAliases[planetSign];

            if (
                planetSignIndex !== undefined
            ) {
                house =
                    ((planetSignIndex -
                        ascSignIndex +
                        12) % 12) + 1;

                planetsByHouse[house].push(
                    String(
                        planet?.name ||
                        planet?.planet ||
                        planet?.body ||
                        "Planet"
                    )
                );
            }
        }
    });

    /* ---------------------------------------------
       BUILD HOUSE CARDS
    --------------------------------------------- */

    const houses = [];

    for (let house = 1; house <= 12; house++) {

        let signIndex = null;

        if (ascSignIndex !== null) {
            signIndex =
                (ascSignIndex +
                    house -
                    1) % 12;
        }

        const sign =
            signIndex !== null
                ? rashiData[signIndex]
                : null;

        houses.push({
            number: house,
            sign,
            planets: planetsByHouse[house]
        });
    }

    /* ---------------------------------------------
       RENDER
    --------------------------------------------- */

    container.innerHTML =
        houses.map(item => {

            const planetsText =
                item.planets.length
                    ? item.planets.join(", ")
                    : "No planets";

            return `
                <article class="house-card">

                    <span class="house-number">
                        ${escapeHtml(item.number)}
                    </span>

                    <div class="house-content">

                        <span class="house-label">
                            HOUSE ${escapeHtml(item.number)}
                        </span>

                        <h3 class="house-title">
                            ${escapeHtml(
                                houseNames[item.number]
                            )}
                        </h3>

                        <div class="house-sign">
                            ${
                                item.sign
                                    ? escapeHtml(
                                        item.sign.name
                                    )
                                    : "—"
                            }
                        </div>

                        <div class="house-lord">
                            Lord:
                            ${
                                item.sign
                                    ? escapeHtml(
                                        item.sign.lord
                                    )
                                    : "—"
                            }
                        </div>

                        <div class="house-planets">
                            <strong>Planets:</strong>
                            ${escapeHtml(
                                planetsText
                            )}
                        </div>

                    </div>

                </article>
            `;
        })
        .join("");
}




    /* ---------------------------------------------------------
       AI ASSISTANT
    --------------------------------------------------------- */

    function initAI() {
        const form =
            $("aiForm");

        if (!form) return;

        form.addEventListener(
            "submit",
            async event => {
                event.preventDefault();

                const input =
                    $("question");

                const answer =
                    $("answer");

                const button =
                    form.querySelector(
                        'button[type="submit"]'
                    );

                if (!input || !answer) {
                    return;
                }

                const question =
                    input.value.trim();

                if (!question) {
                    answer.textContent =
                        "Please enter a question.";
                    return;
                }

                setLoading(
                    button,
                    true,
                    "Thinking..."
                );

                answer.classList.add(
                    "is-loading"
                );

                try {
                    if (
                        window.AIJyotishAI &&
                        typeof window.AIJyotishAI.ask ===
                            "function"
                    ) {
                        const result =
                            await window.AIJyotishAI.ask(
                                question,
                                currentChart
                            );

                        answer.innerHTML =
                            escapeHtml(
                                result?.answer ||
                                result?.response ||
                                result ||
                                "No answer returned."
                            );
                    } else {
                        const result =
                            await apiCall(
                                "/ai/ask",
                                {
                                    method: "POST",
                                    body:
                                        JSON.stringify({
                                            question
                                        })
                                }
                            );

                        answer.textContent =
                            result?.answer ||
                            result?.response ||
                            "No answer returned.";
                    }
                } catch (error) {
                    answer.textContent =
                        error.message ||
                        "Unable to get an AI response.";
                } finally {
                    answer.classList.remove(
                        "is-loading"
                    );

                    setLoading(
                        button,
                        false
                    );
                }
            }
        );
    }

    /* ---------------------------------------------------------
       PRINT
    --------------------------------------------------------- */

    function initPrint() {
        const button =
            $("printBtn");

        if (!button) return;

        button.addEventListener(
            "click",
            event => {
                event.preventDefault();
                window.print();
            }
        );
    }

    /* ---------------------------------------------------------
       PAGE INITIALIZATION
    --------------------------------------------------------- */

    async function initDashboardPage() {
        const page =
            $("dashboardPage");

        if (!page) return;

        try {
            const result =
                await getLatestKundli();

            const chart =
                result?.chart ||
                result?.kundli ||
                result?.data ||
                result;

            if (chart) {
                currentChart = chart;

                sessionStorage.setItem(
                    "aiJyotishLatestChart",
                    JSON.stringify(chart)
                );

                renderDashboard(chart);
            }
        } catch (error) {
            console.error(
                "Dashboard:",
                error
            );
        }
    }

    async function initKundliPage() {
    const page = $("kundliPage");

    if (!page) {
        return;
    }

    let chart = null;

    /*
     * IMPORTANT:
     * First use the chart that was JUST generated.
     * This prevents /kundli/latest from replacing it
     * with an older saved Kundli.
     */
    try {
        const cached =
            sessionStorage.getItem(
                "aiJyotishLatestChart"
            );

        if (cached) {
            const parsed = JSON.parse(cached);

            if (
                parsed &&
                typeof parsed === "object"
            ) {
                chart = parsed;
            }
        }
    } catch (error) {
        console.warn(
            "Could not read cached Kundli:",
            error
        );

        chart = null;
    }

    /*
     * Only use backend /kundli/latest
     * when there is no freshly generated chart.
     */
    if (!chart) {
        try {
            const result =
                await getLatestKundli();

            chart =
                result?.chart ||
                result?.kundli ||
                result?.data ||
                result;
        } catch (error) {
            console.warn(
                "Latest Kundli request failed:",
                error
            );
        }
    }

    if (!chart) {
        console.warn(
            "No Kundli data available."
        );

        return;
    }

    /*
     * Store the chart again so every section
     * uses exactly the same birth chart.
     */
    try {
        sessionStorage.setItem(
            "aiJyotishLatestChart",
            JSON.stringify(chart)
        );
    } catch (error) {
        console.warn(
            "Could not cache Kundli:",
            error
        );
    }

    /*
     * IMPORTANT:
     * Render everything from THIS chart.
     */
    currentChart = chart;

    renderKundli(chart);

    /* Ensure the two derived charts are rendered after the full DOM render. */
    if (
        window.AIJyotishCharts &&
        typeof window.AIJyotishCharts.renderSpecialCharts === "function"
    ) {
        window.AIJyotishCharts.renderSpecialCharts(chart);
    }

    renderHouses(chart);
}

    async function initSessionProtection() {
        const authPages =
            document.body?.dataset?.authPage === "true";

        if (authPages) return;

        const protectedPage =
            $("dashboardPage") ||
            $("kundliPage") ||
            $("birthForm");

        if (!protectedPage) return;

        try {
            const result =
                await getCurrentUser();

            const authenticated =
                result?.authenticated ??
                result?.logged_in ??
                result?.loggedIn ??
                Boolean(
                    result?.user
                );

            if (authenticated === false) {
                redirect("login.html");
            }
        } catch {
            // Do not aggressively redirect if /me
            // is unavailable for a temporary reason.
        }
    }

    function init() {
        initLogin();
        initRegister();
        initBirthForm();
        initLogout();
        initAI();
        initPrint();

        initSessionProtection();

        initDashboardPage();
        initKundliPage();
    }

    /* ---------------------------------------------------------
       PUBLIC API
    --------------------------------------------------------- */

    APP.renderKundli = renderKundli;
    APP.renderDashboard = renderDashboard;
    APP.renderHouses = renderHouses;
    APP.getCurrentChart = () => currentChart;
    APP.logout = logout;

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            init
        );
    } else {
        init();
    }
})();
