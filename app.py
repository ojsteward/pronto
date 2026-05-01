<style>
    /* SECTION CONTAINER */
    .journey-section {
        background-color: #001220;
        color: #ffffff;
        padding: 80px 20px;
        font-family: system-ui, -apple-system, sans-serif;
        text-align: center;
    }

    .journey-title {
        font-size: 42px;
        font-weight: 900;
        margin-bottom: 50px;
        text-transform: uppercase;
        letter-spacing: -1px;
    }

    /* TIMELINE GRID */
    .timeline-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        max-width: 1200px;
        margin: 0 auto 40px;
    }

    .timeline-item {
        background: #ffffff;
        padding: 30px 10px;
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 180px;
    }

    .timeline-year {
        color: #00d2ff;
        font-weight: 800;
        font-size: 20px;
        margin-bottom: 20px;
    }

    .timeline-text {
        color: #333;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .timeline-item.active {
        background: #007a8a; /* Dark Teal from your image */
    }

    .timeline-item.active .timeline-year,
    .timeline-item.active .timeline-text {
        color: #ffffff;
    }

    /* STATS GRID */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .stat-box {
        background: rgba(10, 25, 41, 0.8);
        border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 40px 20px;
        transition: 0.3s;
    }

    .stat-box:hover {
        border-color: #00d2ff;
        background: rgba(0, 210, 255, 0.05);
    }

    .stat-number {
        font-size: 48px;
        font-weight: 900;
        color: #00d2ff;
        margin-bottom: 15px;
        display: block;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
    }

    .stat-desc {
        font-size: 14px;
        line-height: 1.5;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }

    @media (max-width: 768px) {
        .journey-title { font-size: 32px; }
        .timeline-grid { grid-template-columns: 1fr 1fr; }
    }
</style>

<section class="journey-section">
    <h2 class="journey-title">The New Patient Decision Journey</h2>

    <div class="timeline-grid">
        <div class="timeline-item"><span class="timeline-year">1995</span><span class="timeline-text">Yellow Pages</span></div>
        <div class="timeline-item"><span class="timeline-year">2000</span><span class="timeline-text">Word of Mouth</span></div>
        <div class="timeline-item"><span class="timeline-year">2005</span><span class="timeline-text">Internet</span></div>
        <div class="timeline-item"><span class="timeline-year">2010</span><span class="timeline-text">Mobile</span></div>
        <div class="timeline-item"><span class="timeline-year">2015</span><span class="timeline-text">Social Media</span></div>
        <div class="timeline-item"><span class="timeline-year">2020</span><span class="timeline-text">Short-Form Video</span></div>
        <div class="timeline-item active"><span class="timeline-year">2024</span><span class="timeline-text">TIKTOK</span></div>
    </div>

    <div class="stats-grid">
        <!-- 97% -->
        <div class="stat-box">
            <span class="stat-number">97%</span>
            <p class="stat-desc">of people learn more about a local company online than anywhere else</p>
        </div>
        <!-- 84% -->
        <div class="stat-box">
            <span class="stat-number">84%</span>
            <p class="stat-desc">of people trust online reviews as much as a personal recommendation</p>
        </div>
        <!-- 80% -->
        <div class="stat-box">
            <span class="stat-number">80%</span>
            <p class="stat-desc">Video content on a dental website can increase conversion rates by 80%</p>
        </div>
        <!-- 71% -->
        <div class="stat-box">
            <span class="stat-number">71%</span>
            <p class="stat-desc">of patients prefer to book an appointment with a dentist who has an updated website</p>
        </div>
        <!-- 53x -->
        <div class="stat-box">
            <span class="stat-number">53x</span>
            <p class="stat-desc">Pages with video are 53x more likely to rank on the first page of Google</p>
        </div>
        <!-- 50% -->
        <div class="stat-box">
            <span class="stat-number">50%</span>
            <p class="stat-desc">of patients say they are more likely to accept a treatment plan explained via video</p>
        </div>
    </div>
</section>
