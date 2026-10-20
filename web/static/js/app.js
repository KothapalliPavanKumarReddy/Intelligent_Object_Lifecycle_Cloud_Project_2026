/**
 * IntelliArchive — Web Platform Client Logic
 * Handles Chart.js visualization, real-time AI inference UI, and archive filtering.
 */

document.addEventListener("DOMContentLoaded", () => {
    initDashboardCharts();
    initAnalyticsCharts();
    initAnalyzePage();
    initArchiveFilter();
});

// ============================================================================
// 1. CHART.JS VISUALIZATION HELPERS
// ============================================================================

const chartColors = {
    high: '#10b981',
    highAlpha: 'rgba(16, 185, 129, 0.75)',
    medium: '#f59e0b',
    mediumAlpha: 'rgba(245, 158, 11, 0.75)',
    low: '#64748b',
    lowAlpha: 'rgba(100, 116, 139, 0.75)',
    standard: '#6366f1',
    standardAlpha: 'rgba(99, 102, 241, 0.8)',
    ia: '#f59e0b',
    iaAlpha: 'rgba(245, 158, 11, 0.8)',
    glacier: '#06b6d4',
    glacierAlpha: 'rgba(6, 182, 212, 0.8)',
    grid: 'rgba(255, 255, 255, 0.06)',
    text: '#94a3b8'
};

const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: chartColors.text,
                font: { family: 'Inter', size: 12 }
            }
        },
        tooltip: {
            backgroundColor: '#1e293b',
            titleColor: '#f8fafc',
            bodyColor: '#cbd5e1',
            borderColor: '#334155',
            borderWidth: 1,
            padding: 10,
            cornerRadius: 6
        }
    },
    scales: {
        x: {
            grid: { color: chartColors.grid },
            ticks: { color: chartColors.text, font: { family: 'Inter', size: 11 } }
        },
        y: {
            grid: { color: chartColors.grid },
            ticks: { color: chartColors.text, font: { family: 'Inter', size: 11 } }
        }
    }
};

/**
 * Initializes the 3 charts on Page 1 (Dashboard)
 */
async function initDashboardCharts() {
    const scoreCanvas = document.getElementById('dashScoreChart');
    const catCanvas = document.getElementById('dashCategoryChart');
    const storageCanvas = document.getElementById('dashStorageChart');

    if (!scoreCanvas && !catCanvas && !storageCanvas) return;

    try {
        const res = await fetch('/api/analytics');
        if (!res.ok) return;
        const json = await res.json();
        const charts = json.charts;

        // 1. Importance Scores Bar Chart
        if (scoreCanvas && charts.score_chart) {
            const barColors = charts.score_chart.categories.map(cat => {
                if (cat === 'HIGH') return chartColors.highAlpha;
                if (cat === 'MEDIUM') return chartColors.mediumAlpha;
                return chartColors.lowAlpha;
            });

            new Chart(scoreCanvas, {
                type: 'bar',
                data: {
                    labels: charts.score_chart.labels,
                    datasets: [{
                        label: 'Importance Score',
                        data: charts.score_chart.data,
                        backgroundColor: barColors,
                        borderRadius: 4,
                        borderWidth: 1,
                        borderColor: barColors.map(c => c.replace('0.75', '1.0'))
                    }]
                },
                options: {
                    ...defaultChartOptions,
                    scales: {
                        y: {
                            min: 0,
                            max: 100,
                            grid: { color: chartColors.grid },
                            ticks: { color: chartColors.text }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: chartColors.text, maxRotation: 45 }
                        }
                    }
                }
            });
        }

        // 2. Category Distribution Doughnut Chart
        if (catCanvas && charts.category_chart) {
            new Chart(catCanvas, {
                type: 'doughnut',
                data: {
                    labels: charts.category_chart.labels,
                    datasets: [{
                        data: charts.category_chart.data,
                        backgroundColor: [chartColors.high, chartColors.medium, chartColors.low],
                        borderColor: '#111827',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: chartColors.text, padding: 14 }
                        }
                    },
                    cutout: '70%'
                }
            });
        }

        // 3. Storage Distribution Bar Chart
        if (storageCanvas && charts.storage_chart) {
            new Chart(storageCanvas, {
                type: 'bar',
                data: {
                    labels: charts.storage_chart.labels,
                    datasets: [{
                        label: 'Archived Objects',
                        data: charts.storage_chart.data,
                        backgroundColor: [chartColors.standardAlpha, chartColors.iaAlpha, chartColors.glacierAlpha],
                        borderRadius: 6
                    }]
                },
                options: {
                    ...defaultChartOptions,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1, color: chartColors.text },
                            grid: { color: chartColors.grid }
                        },
                        x: { grid: { display: false }, ticks: { color: chartColors.text } }
                    }
                }
            });
        }
    } catch (err) {
        console.error("Dashboard charts error:", err);
    }
}

/**
 * Initializes detailed charts on Page 4 (Analytics)
 */
async function initAnalyticsCharts() {
    const analyticsScoreCanvas = document.getElementById('analyticsScoreChart');
    const analyticsHistCanvas = document.getElementById('analyticsHistogramChart');
    const analyticsCatCanvas = document.getElementById('analyticsCatDonut');
    const analyticsTierCanvas = document.getElementById('analyticsTierDonut');

    if (!analyticsScoreCanvas && !analyticsHistCanvas) return;

    try {
        const res = await fetch('/api/analytics');
        if (!res.ok) return;
        const json = await res.json();
        const charts = json.charts;

        // 1. Detailed Score Ranking Bar Chart
        if (analyticsScoreCanvas && charts.score_chart) {
            const barColors = charts.score_chart.categories.map(cat => {
                if (cat === 'HIGH') return chartColors.high;
                if (cat === 'MEDIUM') return chartColors.medium;
                return chartColors.low;
            });

            new Chart(analyticsScoreCanvas, {
                type: 'bar',
                data: {
                    labels: charts.score_chart.labels,
                    datasets: [{
                        label: 'Semantic Score',
                        data: charts.score_chart.data,
                        backgroundColor: barColors,
                        borderRadius: 4
                    }]
                },
                options: {
                    ...defaultChartOptions,
                    scales: {
                        y: { min: 0, max: 100, grid: { color: chartColors.grid }, ticks: { color: chartColors.text } },
                        x: { grid: { display: false }, ticks: { color: chartColors.text } }
                    }
                }
            });
        }

        // 2. Score Range Histogram
        if (analyticsHistCanvas && charts.histogram_chart) {
            new Chart(analyticsHistCanvas, {
                type: 'bar',
                data: {
                    labels: charts.histogram_chart.labels,
                    datasets: [{
                        label: 'Image Frequency',
                        data: charts.histogram_chart.data,
                        backgroundColor: '#38bdf8',
                        borderRadius: 4
                    }]
                },
                options: {
                    ...defaultChartOptions,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1, color: chartColors.text }, grid: { color: chartColors.grid } },
                        x: { grid: { display: false }, ticks: { color: chartColors.text } }
                    }
                }
            });
        }

        // 3. Category Donut
        if (analyticsCatCanvas && charts.category_chart) {
            new Chart(analyticsCatCanvas, {
                type: 'doughnut',
                data: {
                    labels: charts.category_chart.labels,
                    datasets: [{
                        data: charts.category_chart.data,
                        backgroundColor: [chartColors.high, chartColors.medium, chartColors.low]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: chartColors.text } } },
                    cutout: '65%'
                }
            });
        }

        // 4. Storage Tier Donut
        if (analyticsTierCanvas && charts.storage_chart) {
            new Chart(analyticsTierCanvas, {
                type: 'doughnut',
                data: {
                    labels: charts.storage_chart.labels,
                    datasets: [{
                        data: charts.storage_chart.data,
                        backgroundColor: [chartColors.standard, chartColors.ia, chartColors.glacier]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { color: chartColors.text } } },
                    cutout: '65%'
                }
            });
        }
    } catch (err) {
        console.error("Analytics charts error:", err);
    }
}

// ============================================================================
// 2. INTERACTIVE IMAGE ANALYSIS PAGE LOGIC
// ============================================================================

function initAnalyzePage() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const analyzeBtn = document.getElementById('btnAnalyze');
    const previewContainer = document.getElementById('previewContainer');
    const previewImage = document.getElementById('previewImage');
    const previewFilename = document.getElementById('previewFilename');
    const previewFilesize = document.getElementById('previewFilesize');
    const analysisLoading = document.getElementById('analysisLoading');
    const analysisResultCard = document.getElementById('analysisResultCard');
    const sampleCards = document.querySelectorAll('.sample-pick-card');

    if (!dropzone || !analyzeBtn) return;

    let selectedFile = null;
    let selectedSampleName = null;

    // Drag and drop handlers
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    dropzone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        selectedFile = file;
        selectedSampleName = null;

        // Deselect sample cards
        sampleCards.forEach(c => c.classList.remove('selected'));

        previewFilename.textContent = file.name;
        previewFilesize.textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
        previewContainer.style.display = 'flex';
        analyzeBtn.disabled = false;

        // For image files, preview directly
        if (file.type.startsWith('image/') && !file.name.endsWith('.tif') && !file.name.endsWith('.tiff')) {
            const reader = new FileReader();
            reader.onload = (e) => { previewImage.src = e.target.result; };
            reader.readAsDataURL(file);
        } else {
            // For TIFF files, show satellite icon placeholder until preprocessed
            previewImage.src = '/static/images/satellite_icon.png';
        }
    }

    // Sample Picker Grid handling
    sampleCards.forEach(card => {
        card.addEventListener('click', () => {
            sampleCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');

            selectedSampleName = card.dataset.filename;
            selectedFile = null;

            previewFilename.textContent = selectedSampleName;
            previewFilesize.textContent = card.dataset.filesize || '10.15 MB (TIFF)';
            previewImage.src = `/api/sample-preview/${selectedSampleName}`;
            previewContainer.style.display = 'flex';
            analyzeBtn.disabled = false;
        });
    });

    // Run AI Inference Action
    analyzeBtn.addEventListener('click', async () => {
        if (!selectedFile && !selectedSampleName) return;

        // UI state loading
        analyzeBtn.disabled = true;
        analysisLoading.style.display = 'block';
        analysisResultCard.style.display = 'none';
        const placeholderCard = document.getElementById('initialPlaceholderCard');
        if (placeholderCard) placeholderCard.style.display = 'none';

        // Animate processing stages for UX
        const stageLabel = document.getElementById('processingStageLabel');
        const stages = [
            "1. Ingesting Satellite Pixel Array & Contrast Stretching...",
            "2. Normalizing Dynamic Range & Resizing to 224x224 RGB...",
            "3. Executing OpenAI CLIP ViT-B/32 Zero-Shot Inference...",
            "4. Softmax Weighting & Automated Cloud Storage Tiering..."
        ];

        let stageIdx = 0;
        const stageInterval = setInterval(() => {
            if (stageIdx < stages.length) {
                stageLabel.textContent = stages[stageIdx];
                stageIdx++;
            }
        }, 500);

        try {
            const formData = new FormData();
            if (selectedFile) {
                formData.append('file', selectedFile);
            } else if (selectedSampleName) {
                formData.append('sample_filename', selectedSampleName);
            }
            formData.append('save_to_simulation', 'true');

            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            clearInterval(stageInterval);

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Inference failed');
            }

            const data = await res.json();
            renderAnalysisResult(data);

        } catch (err) {
            clearInterval(stageInterval);
            alert(`Analysis Error: ${err.message}`);
            if (placeholderCard && analysisResultCard.style.display === 'none') {
                placeholderCard.style.display = 'block';
            }
        } finally {
            analysisLoading.style.display = 'none';
            analyzeBtn.disabled = false;
        }
    });

    function renderAnalysisResult(data) {
        const placeholderCard = document.getElementById('initialPlaceholderCard');
        if (placeholderCard) placeholderCard.style.display = 'none';
        analysisResultCard.style.display = 'block';

        // Update score
        document.getElementById('resScoreVal').textContent = data.importance_score.toFixed(2);

        // Update category badge
        const catBadge = document.getElementById('resCategoryBadge');
        catBadge.textContent = data.category;
        catBadge.className = `badge badge-${data.category.toLowerCase()}`;

        // Update storage badge
        const storeBadge = document.getElementById('resStorageBadge');
        storeBadge.textContent = data.storage_class;
        const tierClass = data.storage_class === 'S3_STANDARD' ? 'badge-s3-standard'
            : data.storage_class === 'S3_STANDARD_IA' ? 'badge-s3-ia' : 'badge-s3-glacier';
        storeBadge.className = `badge ${tierClass}`;

        // Model & Status
        document.getElementById('resModelVal').textContent = data.model;
        document.getElementById('resStatusVal').textContent = data.status;

        // Image result preview
        if (data.processed_image_url) {
            document.getElementById('resProcessedImg').src = data.processed_image_url + '?t=' + Date.now();
        }

        // Probabilities
        if (data.probabilities) {
            const pHigh = data.probabilities.high_importance || 0;
            const pMed = data.probabilities.medium_importance || 0;
            const pLow = data.probabilities.low_importance || 0;

            document.getElementById('probHighVal').textContent = pHigh.toFixed(1) + '%';
            document.getElementById('probHighBar').style.width = pHigh + '%';

            document.getElementById('probMedVal').textContent = pMed.toFixed(1) + '%';
            document.getElementById('probMedBar').style.width = pMed + '%';

            document.getElementById('probLowVal').textContent = pLow.toFixed(1) + '%';
            document.getElementById('probLowBar').style.width = pLow + '%';
        }

        // Scroll into view smoothly
        analysisResultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// ============================================================================
// 3. ARCHIVE PAGE FILTERING & MODAL LOGIC
// ============================================================================

function initArchiveFilter() {
    const searchInput = document.getElementById('archiveSearchInput');
    const catPills = document.querySelectorAll('.cat-filter-pill');
    const tierPills = document.querySelectorAll('.tier-filter-pill');
    const items = document.querySelectorAll('.archive-item-card, .archive-table-row');

    if (!searchInput && catPills.length === 0) return;

    let activeCat = 'ALL';
    let activeTier = 'ALL';
    let searchTerm = '';

    function filterItems() {
        items.forEach(el => {
            const itemCat = el.dataset.category || '';
            const itemTier = el.dataset.storage || '';
            const itemName = (el.dataset.name || '').toLowerCase();

            const matchCat = activeCat === 'ALL' || itemCat === activeCat;
            const matchTier = activeTier === 'ALL' || itemTier === activeTier;
            const matchSearch = !searchTerm || itemName.includes(searchTerm);

            if (matchCat && matchTier && matchSearch) {
                el.style.display = '';
            } else {
                el.style.display = 'none';
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchTerm = e.target.value.trim().toLowerCase();
            filterItems();
        });
    }

    catPills.forEach(pill => {
        pill.addEventListener('click', () => {
            catPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            activeCat = pill.dataset.filter;
            filterItems();
        });
    });

    tierPills.forEach(pill => {
        pill.addEventListener('click', () => {
            tierPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            activeTier = pill.dataset.filter;
            filterItems();
        });
    });
}

// Image Detail Modal Handler
window.openImageModal = async function (filename) {
    const modal = document.getElementById('imageModal');
    if (!modal) return;

    try {
        const res = await fetch(`/api/images/${encodeURIComponent(filename)}`);
        if (!res.ok) return;
        const item = await res.json();

        document.getElementById('modalTitle').textContent = item.image_name;
        document.getElementById('modalImage').src = item.thumbnail_url || item.processed_url;
        document.getElementById('modalScore').textContent = item.importance_score.toFixed(2);

        const catBadge = document.getElementById('modalCategory');
        catBadge.textContent = item.category;
        catBadge.className = `badge badge-${item.category.toLowerCase()}`;

        const tierBadge = document.getElementById('modalStorage');
        tierBadge.textContent = item.storage_class;
        const tierClass = item.storage_class === 'S3_STANDARD' ? 'badge-s3-standard'
            : item.storage_class === 'S3_STANDARD_IA' ? 'badge-s3-ia' : 'badge-s3-glacier';
        tierBadge.className = `badge ${tierClass}`;

        document.getElementById('modalSize').textContent = item.file_size_kb + ' KB';
        document.getElementById('modalAction').textContent = item.action;
        document.getElementById('modalSimPath').textContent = `cloud_simulation/${item.storage_class}/${item.image_name}`;

        modal.classList.add('active');
    } catch (err) {
        console.error("Modal fetch error:", err);
    }
};

window.closeImageModal = function () {
    const modal = document.getElementById('imageModal');
    if (modal) modal.classList.remove('active');
};

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        window.closeImageModal();
    }
});


function initS3ArchivePanel() {
    const refreshButton = document.getElementById("refreshS3Button");
    const status = document.getElementById("s3Status");
    const tableBody = document.getElementById("s3ObjectsTableBody");
    const uploadButton = document.getElementById("uploadS3Button");
    const filenameSelect = document.getElementById("s3UploadFilename");

    if (!refreshButton || !status || !tableBody) return;
    if (!uploadButton || !filenameSelect) return;


    refreshButton.addEventListener("click", async () => {
        refreshButton.disabled = true;
        status.textContent = "Loading objects from AWS S3...";
        tableBody.replaceChildren();

        try {
            const response = await fetch("/api/s3/objects");
            let data = null;
            const contentType = response.headers.get("content-type") || "";
            if (contentType.includes("application/json")) {
                data = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || `Server error (${response.status})`);
            }

            if (!response.ok) {
                throw new Error((data && data.detail) || "Unable to load S3 objects.");
            }

            if (!data.success) {
                throw new Error(data.error || "Unable to load S3 objects.");
            }

            status.textContent =
                `${data.count} object(s) found in bucket ${data.bucket}.`;

            if (data.objects.length === 0) {
                const row = tableBody.insertRow();
                const cell = row.insertCell();
                cell.colSpan = 3;
                cell.textContent = "No objects found in this S3 prefix.";
                return;
            }

            data.objects.forEach((object) => {
                const row = tableBody.insertRow();

                const keyCell = row.insertCell();
                keyCell.textContent = object.key;

                const sizeCell = row.insertCell();
                sizeCell.textContent =
                    `${(object.size_bytes / 1024).toFixed(1)} KB`;

                const classCell = row.insertCell();
                classCell.textContent = object.storage_class;
            });
        } catch (error) {
            status.textContent = `S3 error: ${error.message}`;
        } finally {
            refreshButton.disabled = false;
        }
    });

    // Load processed image filenames into the upload dropdown.
    async function loadProcessedImages() {
        filenameSelect.replaceChildren();

        const placeholder = document.createElement("option");
        placeholder.value = "";
        placeholder.textContent = "Loading processed images...";
        filenameSelect.appendChild(placeholder);

        try {
            const response = await fetch("/api/images");
            if (!response.ok) {
                throw new Error("Could not load processed images.");
            }

            const data = await response.json();
            filenameSelect.replaceChildren();

            const images = (data.items || [])
                .filter(item => item.image_name)
                .map(item => item.image_name);

            if (images.length === 0) {
                const option = document.createElement("option");
                option.value = "";
                option.textContent = "No processed images found";
                filenameSelect.appendChild(option);
                return;
            }

            images.forEach(filename => {
                const option = document.createElement("option");
                option.value = filename;
                option.textContent = filename;
                filenameSelect.appendChild(option);
            });
        } catch (error) {
            filenameSelect.replaceChildren();
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "Unable to load images";
            filenameSelect.appendChild(option);
            status.textContent = error.message;
        }
    }

    loadProcessedImages();

    // Upload the selected processed image to real AWS S3.
    uploadButton.addEventListener("click", async () => {
        const filename = filenameSelect.value;

        if (!filename) {
            status.textContent = "Please select a processed image first.";
            return;
        }

        uploadButton.disabled = true;
        status.textContent = `Uploading ${filename} to AWS S3...`;

        try {
            const response = await fetch(
                `/api/s3/upload/${encodeURIComponent(filename)}`,
                { method: "POST" }
            );

            let result = null;
            const contentType = response.headers.get("content-type") || "";
            if (contentType.includes("application/json")) {
                result = await response.json();
            } else {
                const text = await response.text();
                throw new Error(text || `Server error (${response.status})`);
            }

            if (!response.ok) {
                throw new Error((result && result.detail) || "S3 upload failed.");
            }

            const uploadMsg = `Successfully uploaded ${result.object_key} to bucket ${result.bucket}.`;
            status.textContent = uploadMsg;

            // Refresh the real S3 object list and preserve success message
            await refreshButton.click();
            status.textContent = uploadMsg;
        } catch (error) {
            status.textContent = `Upload error: ${error.message}`;
        } finally {
            uploadButton.disabled = false;
        }
    });


}

document.addEventListener("DOMContentLoaded", initS3ArchivePanel);
