import java.util.Properties
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

// Số phiên bản đặt ở android/version.properties (tăng VERSION_CODE mỗi lần phát hành)
val ver = Properties().apply { rootProject.file("version.properties").inputStream().use { load(it) } }
// Khóa ký lấy từ GitHub Secrets lúc build; không có thì ký tạm bằng khóa debug
val ksPath: String? = System.getenv("KEYSTORE_FILE")?.takeIf { file(it).exists() }
val ksPass: String = System.getenv("KEYSTORE_PASSWORD") ?: "onluyennhakhoa"

android {
    namespace = "io.github.tunaasieunhat.onluyennhakhoa.offline"
    compileSdk = 35

    defaultConfig {
        applicationId = "io.github.tunaasieunhat.onluyennhakhoa.offline"
        minSdk = 24
        targetSdk = 35
        versionCode = ver.getProperty("VERSION_CODE").trim().toInt()
        versionName = ver.getProperty("VERSION_NAME").trim()
    }

    signingConfigs {
        if (ksPath != null) {
            create("release") {
                storeFile = file(ksPath)
                storeType = "pkcs12"
                storePassword = ksPass
                keyAlias = System.getenv("KEY_ALIAS") ?: "onluyen"
                keyPassword = ksPass
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = if (ksPath != null) signingConfigs.getByName("release") else signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        buildConfig = true
    }

    androidResources {
        noCompress += listOf("pdf", "woff2")
    }

    lint {
        checkReleaseBuilds = false
        abortOnError = false
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.activity:activity-ktx:1.10.1")
    implementation("androidx.webkit:webkit:1.12.1")
}
