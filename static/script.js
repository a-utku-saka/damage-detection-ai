document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append("image1", document.getElementById("image1").files[0]);
    formData.append("image2", document.getElementById("image2").files[0]);

    // Get the user's selected language
    let selectedLanguage = document.getElementById("language").value;

    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none"; 

    fetch("/detect-damage", {
        method: "POST",
        body: formData,
        headers: {
            "Accept-Language": selectedLanguage // We send the user's selected language as a header
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("loading").style.display = "none";

        if (data.error) {
            document.getElementById("result").innerHTML = `<p style="color: red;">Hata: ${data.error}</p>`;
            document.getElementById("result").style.display = "block";
        } else {
            let damage = data.content.damage;
            let output = `
                <div class="damage-report">
                    <h3>📌 ${selectedLanguage === "tr-tr" ? "Hasar Tespit Raporu" : "Damage Detection Report"}</h3>
                    <p><strong>🔍 ${selectedLanguage === "tr-tr" ? "Hasar Türü" : "Damage Type"}:</strong> ${damage.DamageType || "Bilinmiyor"}</p>
                    <p><strong>🏗️ ${selectedLanguage === "tr-tr" ? "Hasar Kategorisi" : "Damage Category"}:</strong> ${damage.DamageCategory || "Bilinmiyor"}</p>
                    <p><strong>⚠️ ${selectedLanguage === "tr-tr" ? "Hasar Şiddeti" : "Damage Severity"}:</strong> <span class="${(damage.DamageSeverity || "").toLowerCase()}">${damage.DamageSeverity || "Bilinmiyor"}</span></p>
                    <p><strong>📦 ${selectedLanguage === "tr-tr" ? "Kargodan Kaynaklanma Olasılığı" : "Cargo Damage Probability"}:</strong> %${damage.CargoDamageProbability || "Bilinmiyor"}</p>
                    <p><strong>🚛 ${selectedLanguage === "tr-tr" ? "Hasarın Sebebi" : "Cause of Damage"}:</strong> ${damage.DamageCause || "Bilinmiyor"}</p>
                    <p><strong>📋 ${selectedLanguage === "tr-tr" ? "Öneriler" : "Recommendations"}:</strong></p>
                    <ul>
                        ${damage.Recommendations ? damage.Recommendations.map(item => `<li>✅ ${item}</li>`).join("") : "<li>Öneri bulunamadı.</li>"}
                    </ul>
                </div>
            `;
            document.getElementById("result").innerHTML = output;
            document.getElementById("result").style.display = "block";
        }
    })
    .catch(error => {
        console.error("İstek sırasında hata:", error);
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").innerHTML = `<p style="color: red;">Sunucu hatası!</p>`;
        document.getElementById("result").style.display = "block";
    });
});

