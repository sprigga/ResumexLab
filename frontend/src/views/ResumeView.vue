<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useResumeStore } from '@/stores/resume'

const { t, locale } = useI18n()
const resumeStore = useResumeStore()

const loading = ref(true)
// Modified on 2025-11-30: Added state for showing all projects
// Reason: Support collapsing/expanding projects beyond the first 5
const showAllProjects = ref({})
// Added on 2025-11-30: Added state for showing all GitHub projects
// Reason: Support collapsing/expanding GitHub projects beyond the first 5
const showAllGithubProjects = ref(false)

// 已修改於 2025-11-30，原因：新增載入所有履歷資料類型
onMounted(async () => {
  try {
    await Promise.all([
      resumeStore.fetchPersonalInfo().catch(() => null),
      resumeStore.fetchWorkExperiences().catch(() => null),
      resumeStore.fetchProjects().catch(() => null),
      resumeStore.fetchEducation().catch(() => null),
      resumeStore.fetchCertifications().catch(() => null),
      resumeStore.fetchLanguages().catch(() => null),
      resumeStore.fetchPublications().catch(() => null),
      resumeStore.fetchGithubProjects().catch(() => null),
    ])
  } catch (error) {
    console.error('Failed to load resume data:', error)
  } finally {
    loading.value = false
  }
})

const switchLanguage = () => {
  locale.value = locale.value === 'zh-TW' ? 'en-US' : 'zh-TW'
  localStorage.setItem('locale', locale.value)
}

const personalInfo = computed(() => resumeStore.personalInfo)
const workExperiences = computed(() => resumeStore.workExperiences)
// 已新增於 2025-11-30，原因：新增各類履歷資料的 computed properties
const projects = computed(() => resumeStore.projects)
const education = computed(() => resumeStore.education)
const certifications = computed(() => resumeStore.certifications)
const languages = computed(() => resumeStore.languages)
const publications = computed(() => resumeStore.publications)
const githubProjects = computed(() => resumeStore.githubProjects)

// Get localized field
const getField = (obj, fieldPrefix) => {
  if (!obj) return ''
  const suffix = locale.value === 'zh-TW' ? '_zh' : '_en'
  return obj[fieldPrefix + suffix] || obj[fieldPrefix] || ''
}

// Modified on 2025-11-30: Added function to get visible projects (first 5 or all)
// Reason: Support collapsing projects beyond the first 5
const getVisibleProjects = (expId, projects) => {
  if (!projects || projects.length === 0) return []
  if (showAllProjects.value[expId]) {
    return projects
  }
  return projects.slice(0, 5)
}

// Modified on 2025-11-30: Added function to toggle showing all projects
// Reason: Support collapsing/expanding projects
const toggleShowAllProjects = (expId) => {
  showAllProjects.value[expId] = !showAllProjects.value[expId]
}

// Modified on 2025-11-30: Added function to get visible GitHub projects (first 5 or all)
// Reason: Support collapsing GitHub projects beyond the first 5
const getVisibleGithubProjects = (projects) => {
  if (!projects || projects.length === 0) return []
  if (showAllGithubProjects.value) {
    return projects
  }
  return projects.slice(0, 5)
}

// Modified on 2025-11-30: Added function to toggle showing all GitHub projects
// Reason: Support collapsing/expanding GitHub projects
const toggleShowAllGithubProjects = () => {
  showAllGithubProjects.value = !showAllGithubProjects.value
}
</script>

<template>
  <div class="resume-container">
    <!-- Language Switcher -->
    <div class="language-switcher">
      <el-button @click="switchLanguage" type="primary" size="small">
        {{ locale === 'zh-TW' ? 'EN' : '中文' }}
      </el-button>
    </div>

    <el-card v-loading="loading" class="resume-card">
      <!-- Personal Information -->
      <div v-if="personalInfo" class="section">
        <!-- Header with photo and personal info - Added on 2025-11-29 -->
        <!-- Reason: Arranging photo on the right with vertically stacked contact info -->
        <div class="header-container">
          <div class="contact-info-vertical">
            <h1 class="name">{{ getField(personalInfo, 'name') }}</h1>
            <p v-if="personalInfo.email">
              <el-icon><Message /></el-icon> {{ personalInfo.email }}
            </p>
            <p v-if="personalInfo.phone">
              <el-icon><Phone /></el-icon> {{ personalInfo.phone }}
            </p>
            <p v-if="getField(personalInfo, 'address')">
              <el-icon><Location /></el-icon> {{ getField(personalInfo, 'address') }}
            </p>
          </div>
          <div class="photo-container">
            <img src="/media/IMG_7559.PNG" alt="Profile Photo" class="profile-photo" />
          </div>
        </div>

        <div v-if="getField(personalInfo, 'objective')" class="objective">
          <h2>{{ t('resume.objective') }}</h2>
          <p>{{ getField(personalInfo, 'objective') }}</p>
        </div>

        <div v-if="getField(personalInfo, 'summary')" class="summary">
          <h2>{{ t('resume.summary') }}</h2>
          <p>{{ getField(personalInfo, 'summary') }}</p>
        </div>
      </div>

      <!-- Work Experience -->
      <!-- Modified on 2025-11-30: Added projects display under each work experience -->
      <!-- Reason: Projects are now child records of work experience -->
      <div v-if="workExperiences.length" class="section">
        <h2 class="section-title">{{ t('resume.workExperience') }}</h2>
        <div v-for="exp in workExperiences" :key="exp.id" class="experience-item">
          <div class="exp-header">
            <div>
              <h3 class="company">{{ getField(exp, 'company') }}</h3>
              <p class="position">{{ getField(exp, 'position') }}</p>
            </div>
            <div class="date-location">
              <p class="date">
                {{ exp.start_date }} - {{ exp.is_current ? t('resume.current') : exp.end_date }}
              </p>
              <p class="location">{{ getField(exp, 'location') }}</p>
            </div>
          </div>
          <p v-if="getField(exp, 'description')" class="description">
            {{ getField(exp, 'description') }}
          </p>

          <!-- Projects under this work experience -->
          <!-- Modified on 2025-11-30: Display only first 5 projects, with expand/collapse button -->
          <!-- Reason: User requested to show first 5 projects and collapse the rest -->
          <div v-if="exp.projects && exp.projects.length > 0" class="projects-list">
            <div v-for="project in getVisibleProjects(exp.id, exp.projects)" :key="project.id" class="project-item">
              <div class="project-header">
                <h4 class="project-title">{{ getField(project, 'title') }}</h4>
                <p class="project-date">
                  {{ project.start_date || 'N/A' }} - {{ project.end_date || 'Present' }}
                </p>
              </div>
              <p v-if="getField(project, 'description')" class="project-description">
                {{ getField(project, 'description') }}
              </p>
              <div v-if="project.technologies || project.tools" class="project-tech">
                <span v-if="project.technologies"><strong>Technologies:</strong> {{ project.technologies }}</span>
                <span v-if="project.tools"><strong>Tools:</strong> {{ project.tools }}</span>
              </div>
            </div>

            <!-- Show expand/collapse button if more than 5 projects -->
            <div v-if="exp.projects.length > 5" class="show-all-button-container">
              <el-button
                @click="toggleShowAllProjects(exp.id)"
                type="primary"
                size="small"
                plain
              >
                {{ showAllProjects[exp.id] ? t('resume.showLess') : t('resume.showAll') }}
                ({{ showAllProjects[exp.id] ? '-' : '+' }}{{ exp.projects.length - 5 }})
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- Projects Section - Commented out on 2025-11-30 -->
      <!-- Reason: Projects are now displayed under each work experience instead of separate section -->
      <!-- <div v-if="projects.length" class="section">
        <h2 class="section-title">Projects</h2>
        <div v-for="project in projects" :key="project.id" class="experience-item">
          <div class="exp-header">
            <div>
              <h3 class="company">{{ getField(project, 'title') }}</h3>
            </div>
            <div class="date-location">
              <p class="date">
                {{ project.start_date || 'N/A' }} - {{ project.end_date || 'Present' }}
              </p>
            </div>
          </div>
          <p v-if="getField(project, 'description')" class="description">
            {{ getField(project, 'description') }}
          </p>
          <div v-if="project.technologies || project.tools" class="project-tech">
            <span v-if="project.technologies"><strong>Technologies:</strong> {{ project.technologies }}</span>
            <span v-if="project.tools"><strong>Tools:</strong> {{ project.tools }}</span>
          </div>
        </div>
      </div> -->

      <!-- Education Section - 已新增於 2025-11-30 -->
      <div v-if="education.length" class="section">
        <h2 class="section-title">{{ t('resume.education') }}</h2>
        <div v-for="edu in education" :key="edu.id" class="experience-item">
          <div class="exp-header">
            <div>
              <h3 class="company">{{ getField(edu, 'school') }}</h3>
              <p class="position">{{ getField(edu, 'degree') }} - {{ getField(edu, 'major') }}</p>
            </div>
            <div class="date-location">
              <p class="date">{{ edu.start_date }} - {{ edu.end_date }}</p>
            </div>
          </div>
          <p v-if="getField(edu, 'description')" class="description">
            {{ getField(edu, 'description') }}
          </p>
        </div>
      </div>

      <!-- Certifications Section - 已新增於 2025-11-30 -->
      <div v-if="certifications.length" class="section">
        <h2 class="section-title">{{ t('resume.certifications') }}</h2>
        <div class="cert-grid">
          <div v-for="cert in certifications" :key="cert.id" class="cert-item">
            <h4>{{ getField(cert, 'name') }}</h4>
            <p class="cert-issuer">{{ cert.issuer }}</p>
            <p class="cert-date">{{ cert.issue_date }}</p>
            <p v-if="cert.certificate_number" class="cert-number">{{ cert.certificate_number }}</p>
          </div>
        </div>
      </div>

      <!-- Languages Section - 已新增於 2025-11-30 -->
      <div v-if="languages.length" class="section">
        <h2 class="section-title">{{ t('resume.languages') }}</h2>
        <div class="lang-grid">
          <div v-for="lang in languages" :key="lang.id" class="lang-item">
            <h4>{{ getField(lang, 'language') }}</h4>
            <p class="lang-proficiency">{{ getField(lang, 'proficiency') }}</p>
            <p v-if="lang.test_name" class="lang-test">{{ lang.test_name }}: {{ lang.score }}</p>
          </div>
        </div>
      </div>

      <!-- Publications Section - 已新增於 2025-11-30 -->
      <div v-if="publications.length" class="section">
        <h2 class="section-title">{{ t('resume.publications') }}</h2>
        <div v-for="pub in publications" :key="pub.id" class="pub-item">
          <p class="pub-title">{{ pub.title }}</p>
          <p class="pub-authors">{{ pub.authors }}</p>
          <p class="pub-details">{{ pub.publication }}, {{ pub.year }}, pp. {{ pub.pages }}</p>
        </div>
      </div>

      <!-- GitHub Projects Section - 已新增於 2025-11-30 -->
      <!-- Modified on 2025-11-30: Display only first 5 GitHub projects, with expand/collapse button -->
      <!-- Reason: User requested to show first 5 projects and collapse the rest -->
      <div v-if="githubProjects.length" class="section">
        <h2 class="section-title">{{ t('resume.githubProjects') }}</h2>
        <div v-for="gh in getVisibleGithubProjects(githubProjects)" :key="gh.id" class="github-item">
          <h4>{{ getField(gh, 'name') }}</h4>
          <p class="description">{{ getField(gh, 'description') }}</p>
          <a v-if="gh.url" :href="gh.url" target="_blank" class="github-link">{{ gh.url }}</a>
        </div>

        <!-- Show expand/collapse button if more than 5 GitHub projects -->
        <div v-if="githubProjects.length > 5" class="show-all-button-container">
          <el-button
            @click="toggleShowAllGithubProjects"
            type="primary"
            size="small"
            plain
          >
            {{ showAllGithubProjects ? t('resume.showLess') : t('resume.showAll') }}
            ({{ showAllGithubProjects ? '-' : '+' }}{{ githubProjects.length - 5 }})
          </el-button>
        </div>
      </div>

      <!-- Empty State -->
      <el-empty v-if="!loading && !personalInfo" description="No resume data available" />
    </el-card>
  </div>
</template>

<style scoped>
/* Applying global styles from style.css - Updated on 2025-11-29 */
/* Reason: Ensuring resume-container background matches style.css global background */
/* Updated on 2025-11-30 - Changed max-width from 900px to 1200px */
/* Reason: User requested wider layout to accommodate full publication titles */
.resume-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  /* Gradient background from black to deep blue to gray - matches style.css */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
  color: rgba(255, 255, 255, 0.87);
  position: relative;
}

/* Vignette effect - subtle inner shadow */
.resume-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  box-shadow: inset 0 0 200px rgba(0, 0, 0, 0.5);
  z-index: 0;
}

/* Ensure content is above vignette */
.resume-container > * {
  position: relative;
  z-index: 1;
}

/* Language switcher styling - Updated on 2025-11-29 */
/* Reason: Ensure button is visible on dark gradient background */
.language-switcher {
  text-align: right;
  margin-bottom: 20px;
}

.language-switcher :deep(.el-button) {
  background-color: #646cff !important;
  border-color: #646cff !important;
  color: white !important;
}

.language-switcher :deep(.el-button:hover) {
  background-color: #535bf2 !important;
  border-color: #535bf2 !important;
}

.resume-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  padding: 2em;
  /* Original background - commented out on 2025-11-29 */
  /* Reason: Making card background consistent with outer gradient background */
  /* background-color: rgba(255, 255, 255, 0.95); */
  /* backdrop-filter: blur(10px); */

  /* New background matching the gradient - Updated on 2025-11-29 */
  /* Reason: Ensuring card background matches the overall gradient background */
  background: linear-gradient(to bottom, #000000 0%, #1a2332 50%, #404040 100%) !important;
  color: rgba(255, 255, 255, 0.87) !important;
  border: none !important;
}

.section {
  margin-bottom: 30px;
}

/* Header container with photo - Added on 2025-11-29 */
/* Reason: Horizontal layout for contact info and photo */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
  margin-bottom: 20px;
}

/* Contact info vertical layout - Added on 2025-11-29 */
/* Reason: Stacking name, email, phone, address vertically */
/* Updated on 2025-11-29 - Removed justify-content center, added align-items flex-start */
/* Reason: All items should be left-aligned and vertically stacked */
.contact-info-vertical {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}

/* Updated on 2025-11-29 - Removed margin to align vertically with contact info */
/* Reason: Name should be vertically aligned with email, phone, address */
.contact-info-vertical .name {
  font-size: 3.2em;
  line-height: 1.1;
  font-weight: bold;
  margin: 0;
  padding: 0;
  color: rgba(255, 255, 255, 0.95);
  text-align: left;
}

.contact-info-vertical p {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.75);
  margin: 0;
  padding: 0;
  font-size: 16px;
  text-align: left;
}

/* Photo container - Added on 2025-11-29 */
/* Reason: Positioning photo on the right side */
.photo-container {
  flex-shrink: 0;
}

.profile-photo {
  width: 180px;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Original styles - commented out on 2025-11-29 */
/* Reason: Replaced with new header-container layout */
/* .name {
  font-size: 3.2em;
  line-height: 1.1;
  font-weight: bold;
  margin-bottom: 10px;
  color: rgba(255, 255, 255, 0.95);
}

.contact-info {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  color: rgba(255, 255, 255, 0.75);
}

.contact-info p {
  display: flex;
  align-items: center;
  gap: 5px;
} */

.objective,
.summary {
  margin-top: 20px;
}

/* Objective and Summary h2 styling - Added on 2025-11-29 */
/* Reason: Unifying all section titles to use consistent white text color */
.objective h2,
.summary h2,
.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 15px;
  color: rgba(255, 255, 255, 0.95) !important;
  border-bottom: 2px solid #646cff;
  padding-bottom: 5px;
}

/* Objective and Summary paragraph styling - Added on 2025-11-29 */
/* Reason: Explicitly set paragraph color to match description text */
/* Updated on 2025-11-29 - Added text-align: left */
.objective p,
.summary p {
  color: rgba(255, 255, 255, 0.87);
  line-height: 1.6;
  font-size: 16px;
  text-align: left;
}

.experience-item {
  margin-bottom: 25px;
  padding-bottom: 25px;
  /* Original border - commented out on 2025-11-29 */
  /* Reason: Adjusting border color for dark gradient background */
  /* border-bottom: 1px solid #ebeef5; */
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.experience-item:last-child {
  border-bottom: none;
}

/* Element Plus loading overlay customization - Added on 2025-11-29 */
/* Reason: Make loading overlay background transparent to match gradient */
.resume-card :deep(.el-loading-mask) {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

.exp-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.company {
  font-size: 20px;
  font-weight: bold;
  /* Original color - commented out on 2025-11-29 */
  /* Reason: Adjusting text color for dark gradient background */
  /* color: #2c3e50; */
  /* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.95) to #4a69bd */
  /* Reason: User requested blue color for company name */
  /* color: #4a69bd; */
  /* Updated on 2025-11-30 - Changed to brighter blue #6c8cd5 */
  /* Reason: User requested higher contrast and brightness for better visibility */
  /* color: #6c8cd5; */
  /* Updated on 2025-11-30 - Changed to very bright cyan-blue #8FB8ED with !important */
  /* Reason: User confirmed text still not visible enough, using brighter color with !important to override any conflicts */
  color: #8FB8ED !important;
  margin-bottom: 5px;
}

.position {
  font-size: 16px;
  /* Original color - commented out on 2025-11-29 */
  /* Reason: Adjusting text color for dark gradient background */
  /* color: #606266; */
  /* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.8) to #d0d0d0 */
  /* Reason: User requested lighter gray color for position */
  /* color: #d0d0d0; */
  /* Updated on 2025-11-30 - Changed to brighter gray #e8e8e8 */
  /* Reason: User requested higher contrast and brightness for better visibility */
  /* color: #e8e8e8; */
  /* Updated on 2025-11-30 - Changed to very bright white #F5F5F5 with !important */
  /* Reason: User confirmed text still not visible enough, using near-white color with !important to override any conflicts */
  color: #F5F5F5 !important;
  font-weight: 500;
}

.date-location {
  text-align: right;
  /* Original color - commented out on 2025-11-29 */
  /* Reason: Adjusting text color for dark gradient background */
  /* color: #909399; */
  color: rgba(255, 255, 255, 0.65);
}

.date {
  font-size: 14px;
  margin-bottom: 3px;
}

.location {
  font-size: 14px;
}

.description {
  /* Original color - commented out on 2025-11-29 */
  /* Reason: Adjusting text color for dark gradient background */
  /* color: #606266; */
  /* Updated on 2025-11-29 to match summary paragraph style - THIRD UPDATE */
  /* Reason: Work experience description should match summary/objective paragraph brightness */
  /* Previous attempts: 0.8 (too dim), 0.87 (still overridden) */
  /* Adding !important to override any conflicting styles */
  color: rgba(255, 255, 255, 0.87) !important;
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 16px;
  /* Added on 2025-11-29 - Set text alignment to left */
  text-align: left;
}

@media (max-width: 768px) {
  .exp-header {
    flex-direction: column;
  }

  .date-location {
    text-align: left;
    margin-top: 5px;
  }

  /* Original contact-info mobile styles - commented out on 2025-11-29 */
  /* Reason: Replaced with header-container mobile layout */
  /* .contact-info {
    flex-direction: column;
    gap: 10px;
  } */

  /* Header container mobile layout - Added on 2025-11-29 */
  /* Reason: Stack photo and contact info vertically on mobile */
  .header-container {
    flex-direction: column-reverse;
    align-items: center;
    gap: 20px;
  }

  .contact-info-vertical {
    text-align: center;
    align-items: center;
  }

  .photo-container {
    margin-bottom: 10px;
  }

  .profile-photo {
    width: 150px;
    height: 150px;
  }
}

/* Light mode specific styles */
@media (prefers-color-scheme: light) {
  .resume-container {
    color: #213547;
    /* Light mode: use white background instead of gradient */
    background: #ffffff;
  }

  .resume-container::before {
    /* Remove vignette in light mode */
    display: none;
  }

  .resume-card {
    background: #ffffff;
    color: #213547;
  }

  .name,
  .section-title,
  .company {
    color: #213547;
  }

  .objective h2,
  .summary h2 {
    color: #213547;
  }

  .contact-info {
    color: #606266;
  }

  .position {
    color: #606266;
  }

  .date-location {
    color: #909399;
  }

  .description {
    /* Updated on 2025-11-29 to match summary paragraph in light mode */
    color: #606266;
    font-size: 16px;
  }

  .experience-item {
    border-bottom: 1px solid #ebeef5;
  }
}

/* New sections styles - Added on 2025-11-30 */
/* Reason: Styling for newly added resume sections */

/* Projects list within work experience - Added on 2025-11-30 */
/* Reason: Display projects as child records under work experience */
.projects-list {
  margin-top: 20px;
  margin-left: 20px;
  border-left: 3px solid #646cff;
  padding-left: 20px;
}

.project-item {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.project-item:last-child {
  border-bottom: none;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.95) to #8FB8ED */
/* Reason: User requested higher contrast and brightness for better visibility */
.project-title {
  font-size: 18px;
  font-weight: 600;
  color: #8FB8ED !important;
  margin: 0;
}

.project-date {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
  margin: 0;
  white-space: nowrap;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.87) to #F5F5F5 */
/* Reason: User requested higher contrast and brightness for better visibility */
.project-description {
  color: #F5F5F5 !important;
  line-height: 1.6;
  font-size: 15px;
  text-align: left;
  margin: 8px 0;
}

/* Project technology tags */
/* Updated on 2025-11-30 - Improved contrast for Technologies and Tools text */
/* Reason: User requested higher contrast and brightness for better visibility */
.project-tech {
  margin-top: 10px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  color: #E8E8E8 !important;
  font-size: 14px;
}

.project-tech strong {
  color: #8FB8ED !important;
}

/* Certifications grid */
/* Updated on 2025-11-30 - Changed background from white to gradient style */
/* Reason: User requested matching grid colors with overall gradient background */
.cert-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.cert-item {
  padding: 15px;
  border: 1px solid rgba(100, 108, 255, 0.3) !important;
  border-radius: 8px;
  /* Changed from white background to gradient matching overall style */
  background: linear-gradient(135deg, rgba(26, 35, 50, 0.6) 0%, rgba(64, 64, 64, 0.4) 100%) !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.3s ease;
}

.cert-item:hover {
  border-color: rgba(100, 108, 255, 0.5);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

.cert-item h4 {
  margin: 0 0 10px 0;
  color: #8FB8ED !important;
  font-size: 16px;
  font-weight: 600;
}

.cert-issuer,
.cert-date,
.cert-number {
  margin: 5px 0;
  color: #E8E8E8 !important;
  font-size: 14px;
}

/* Languages grid */
/* Updated on 2025-11-30 - Changed background from white to gradient style */
/* Reason: User requested matching grid colors with overall gradient background */
.lang-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.lang-item {
  padding: 15px;
  border: 1px solid rgba(100, 108, 255, 0.3) !important;
  border-radius: 8px;
  /* Changed from white background to gradient matching overall style */
  background: linear-gradient(135deg, rgba(26, 35, 50, 0.6) 0%, rgba(64, 64, 64, 0.4) 100%) !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.3s ease;
}

.lang-item:hover {
  border-color: rgba(100, 108, 255, 0.5);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

.lang-item h4 {
  margin: 0 0 8px 0;
  color: #8FB8ED !important;
  font-size: 16px;
  font-weight: 600;
}

.lang-proficiency,
.lang-test {
  margin: 5px 0;
  color: #E8E8E8 !important;
  font-size: 14px;
}

/* Publications */
/* Updated on 2025-11-30 - Improved contrast for publication text */
/* Reason: User requested higher contrast and brightness for better visibility */
.pub-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.pub-item:last-child {
  border-bottom: none;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.95) to #8FB8ED */
/* Reason: Using consistent bright cyan-blue for titles to match other sections */
/* Updated on 2025-11-30 - Added text-align: left */
/* Reason: User requested left alignment for publication text */
.pub-title {
  font-weight: bold;
  color: #8FB8ED !important;
  font-size: 16px;
  margin-bottom: 5px;
  text-align: left;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.8) to #E8E8E8 */
/* Reason: Using brighter gray for better visibility of author names */
/* Updated on 2025-11-30 - Added text-align: left */
/* Reason: User requested left alignment for publication text */
.pub-authors {
  color: #E8E8E8 !important;
  font-style: italic;
  margin-bottom: 5px;
  text-align: left;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.75) to #D0D0D0 */
/* Reason: Using brighter gray for better visibility of publication details */
/* Updated on 2025-11-30 - Added text-align: left */
/* Reason: User requested left alignment for publication text */
.pub-details {
  color: #D0D0D0 !important;
  font-size: 14px;
  text-align: left;
}

/* GitHub Projects */
/* Updated on 2025-11-30 - Improved contrast for GitHub project name and link */
/* Reason: User requested higher contrast and brightness with left alignment */
.github-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.github-item:last-child {
  border-bottom: none;
}

/* Updated on 2025-11-30 - Changed from rgba(255, 255, 255, 0.95) to #8FB8ED with left alignment */
/* Reason: Using consistent bright cyan-blue for project names to match other section titles */
.github-item h4 {
  margin: 0 0 8px 0;
  color: #8FB8ED !important;
  font-size: 18px;
  text-align: left;
}

/* Updated on 2025-11-30 - Changed from #646cff to #A8C5F0 for better visibility */
/* Reason: Using brighter cyan-blue for better contrast on dark background with left alignment */
.github-link {
  color: #A8C5F0 !important;
  text-decoration: none;
  font-size: 14px;
  text-align: left;
  display: block;
}

.github-link:hover {
  text-decoration: underline;
  color: #C0D8FF !important;
}

/* Show all button container - Added on 2025-11-30 */
/* Reason: Center the expand/collapse button for projects */
.show-all-button-container {
  margin-top: 15px;
  text-align: center;
}

.show-all-button-container :deep(.el-button) {
  background-color: rgba(100, 108, 255, 0.2) !important;
  border-color: #646cff !important;
  color: #8FB8ED !important;
  transition: all 0.3s ease;
}

.show-all-button-container :deep(.el-button:hover) {
  background-color: rgba(100, 108, 255, 0.4) !important;
  border-color: #8FB8ED !important;
  color: #C0D8FF !important;
}

/* Light mode adjustments for new sections */
@media (prefers-color-scheme: light) {
  .show-all-button-container :deep(.el-button) {
    background-color: #f0f2ff !important;
    border-color: #646cff !important;
    color: #646cff !important;
  }

  .show-all-button-container :deep(.el-button:hover) {
    background-color: #e0e4ff !important;
    border-color: #535bf2 !important;
    color: #535bf2 !important;
  }

  .projects-list {
    border-left-color: #646cff;
  }

  .project-item {
    border-bottom: 1px solid #ebeef5;
  }

  .project-title {
    color: #2c3e50;
  }

  .project-date {
    color: #909399;
  }

  .project-description {
    color: #606266;
  }

  .project-tech {
    color: #606266;
  }

  .project-tech strong {
    color: #2c3e50;
  }

  .cert-item,
  .lang-item {
    border: 1px solid #ebeef5;
    background: #f9f9f9;
  }

  .cert-item h4,
  .lang-item h4,
  .pub-title,
  .github-item h4 {
    color: #2c3e50;
  }

  .cert-issuer,
  .cert-date,
  .cert-number,
  .lang-proficiency,
  .lang-test,
  .pub-authors,
  .pub-details {
    color: #606266;
  }

  .pub-item,
  .github-item {
    border-bottom: 1px solid #ebeef5;
  }

  .github-link {
    color: #646cff;
  }
}
</style>
