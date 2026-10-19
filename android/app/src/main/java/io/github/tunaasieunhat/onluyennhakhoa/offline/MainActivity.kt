package io.github.tunaasieunhat.onluyennhakhoa.offline

import android.annotation.SuppressLint
import android.app.AlertDialog
import android.content.ActivityNotFoundException
import android.content.ContentValues
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.SystemClock
import android.provider.MediaStore
import android.util.Base64
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.SystemBarStyle
import androidx.activity.enableEdgeToEdge
import androidx.core.content.FileProvider
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.webkit.WebViewAssetLoader
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

/**
 * Ôn Luyện Nha Khoa (bản app Android, version 1.0).
 * Toàn bộ giao diện, câu hỏi, tóm tắt và PDF nằm sẵn trong app (thư mục assets/www),
 * được hiển thị bằng bộ hiển thị web có sẵn của Android nên không cần mở Chrome hay có mạng.
 */
class MainActivity : ComponentActivity() {

    private lateinit var web: WebView
    private var lastBack = 0L

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge(
            statusBarStyle = SystemBarStyle.dark(Color.TRANSPARENT),
            navigationBarStyle = SystemBarStyle.dark(Color.TRANSPARENT)
        )
        super.onCreate(savedInstanceState)

        val root = FrameLayout(this)
        root.setBackgroundColor(BRAND)
        web = WebView(this)
        web.setBackgroundColor(WALL)
        root.addView(
            web,
            FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
        )
        setContentView(root)

        // Chừa chỗ cho thanh trạng thái, thanh điều hướng, tai thỏ và bàn phím
        ViewCompat.setOnApplyWindowInsetsListener(root) { v, insets ->
            val bars = insets.getInsets(
                WindowInsetsCompat.Type.systemBars() or
                    WindowInsetsCompat.Type.displayCutout() or
                    WindowInsetsCompat.Type.ime()
            )
            v.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            WindowInsetsCompat.CONSUMED
        }

        setupWebView()
        if (savedInstanceState == null || web.restoreState(savedInstanceState) == null) {
            web.loadUrl(START_URL)
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() = onBack()
        })

        web.postDelayed({ checkUpdate() }, 4000)
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val loader = WebViewAssetLoader.Builder()
            .setDomain(HOST)
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this))
            .build()

        web.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            mediaPlaybackRequiresUserGesture = false
            allowFileAccess = false
            allowContentAccess = false
            setSupportZoom(false)
            builtInZoomControls = false
            displayZoomControls = false
            textZoom = 100
            useWideViewPort = true
            userAgentString = "$userAgentString OnLuyenNhaKhoaApp/${BuildConfig.VERSION_NAME}"
        }
        web.addJavascriptInterface(Bridge(), "AndroidApp")
        web.webChromeClient = WebChromeClient()
        web.webViewClient = object : WebViewClient() {
            override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                val url = request?.url ?: return null
                return loader.shouldInterceptRequest(url)
            }

            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url ?: return false
                if (url.host == HOST) return false
                // Link ra ngoài (email, trang web…) thì mở bằng ứng dụng khác
                openExternal(url)
                return true
            }
        }
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)
    }

    /** Nút Quay lại: đóng hộp thoại / về màn trước trong app; ở sảnh thì bấm 2 lần để thoát. */
    private fun onBack() {
        web.evaluateJavascript(
            "(function(){try{return window.__androidBack&&window.__androidBack()?1:0}catch(e){return 0}})()"
        ) { result ->
            if (result == "1") return@evaluateJavascript
            val now = SystemClock.elapsedRealtime()
            if (now - lastBack < 2000) {
                moveTaskToBack(true)
            } else {
                lastBack = now
                Toast.makeText(this, "Bấm Quay lại lần nữa để thoát", Toast.LENGTH_SHORT).show()
            }
        }
    }

    /** Cầu nối cho trang: lưu file PDF / ảnh sơ đồ vào thư mục Tải xuống. */
    inner class Bridge {
        @JavascriptInterface
        fun saveFile(name: String?, mime: String?, base64: String?): String {
            if (name.isNullOrBlank() || base64.isNullOrEmpty()) return "error"
            return try {
                val clean = cleanName(name)
                val type = if (mime.isNullOrBlank()) "application/octet-stream" else mime
                val uri = writeDownload(clean, type, Base64.decode(base64, Base64.DEFAULT))
                runOnUiThread { showSaved(clean, type, uri) }
                "saved"
            } catch (e: Exception) {
                "error"
            }
        }

        @JavascriptInterface
        fun appVersion(): String = BuildConfig.VERSION_NAME
    }

    private fun cleanName(name: String): String =
        name.replace(Regex("[\\\\/:*?\"<>|]"), "_").trim().take(120).ifBlank { "file" }

    private fun writeDownload(name: String, mime: String, bytes: ByteArray): Uri {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val resolver = contentResolver
            val values = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, name)
                put(MediaStore.MediaColumns.MIME_TYPE, mime)
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/" + FOLDER)
                put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
            val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values)
                ?: throw IOException("insert failed")
            try {
                val out = resolver.openOutputStream(uri) ?: throw IOException("open failed")
                out.use { it.write(bytes) }
                values.clear()
                values.put(MediaStore.MediaColumns.IS_PENDING, 0)
                resolver.update(uri, values, null, null)
            } catch (e: Exception) {
                resolver.delete(uri, null, null)
                throw e
            }
            return uri
        }
        // Android 9 trở xuống: lưu trong thư mục riêng của app, mở được bằng nút "Mở"
        val dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS) ?: File(filesDir, "Download")
        dir.mkdirs()
        val file = File(dir, name)
        file.writeBytes(bytes)
        return FileProvider.getUriForFile(this, "$packageName.files", file)
    }

    private fun showSaved(name: String, mime: String, uri: Uri) {
        if (isFinishing || isDestroyed) return
        val where = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) "Tải xuống › $FOLDER" else "riêng của app"
        AlertDialog.Builder(this)
            .setTitle("Đã lưu file")
            .setMessage("$name\n\nFile nằm trong thư mục $where.")
            .setPositiveButton("Mở") { _, _ -> openFile(uri, mime) }
            .setNegativeButton("Đóng", null)
            .show()
    }

    private fun openFile(uri: Uri, mime: String) {
        val intent = Intent(Intent.ACTION_VIEW)
            .setDataAndType(uri, mime)
            .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            startActivity(intent)
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(this, "Máy chưa có ứng dụng mở được file này.", Toast.LENGTH_LONG).show()
        }
    }

    private fun openExternal(uri: Uri) {
        try {
            startActivity(Intent(Intent.ACTION_VIEW, uri).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(this, "Không mở được liên kết này.", Toast.LENGTH_SHORT).show()
        }
    }

    /** Có mạng thì xem trên GitHub có bản APK mới hơn không (tối đa 6 giờ một lần). */
    private fun checkUpdate() {
        val prefs = getSharedPreferences("app", MODE_PRIVATE)
        val now = System.currentTimeMillis()
        if (now - prefs.getLong("lastCheck", 0L) < 6L * 60 * 60 * 1000) return
        val current = BuildConfig.VERSION_CODE.toLong()
        thread(isDaemon = true) {
            try {
                val conn = URL(RELEASE_API).openConnection() as HttpURLConnection
                conn.connectTimeout = 8000
                conn.readTimeout = 8000
                conn.setRequestProperty("Accept", "application/vnd.github+json")
                conn.setRequestProperty("User-Agent", "OnLuyenNhaKhoaApp")
                if (conn.responseCode != 200) return@thread
                val json = JSONObject(conn.inputStream.bufferedReader().use { it.readText() })
                prefs.edit().putLong("lastCheck", now).apply()
                val code = Regex("^apk-(\\d+)$").find(json.optString("tag_name"))
                    ?.groupValues?.get(1)?.toLongOrNull() ?: return@thread
                if (code <= current) return@thread
                var link = json.optString("html_url")
                val assets = json.optJSONArray("assets")
                if (assets != null) {
                    for (i in 0 until assets.length()) {
                        val a = assets.optJSONObject(i) ?: continue
                        if (a.optString("name").endsWith(".apk")) {
                            link = a.optString("browser_download_url", link)
                            break
                        }
                    }
                }
                val title = json.optString("name").ifBlank { "Bản mới" }
                val notes = json.optString("body").take(600)
                runOnUiThread { showUpdate(title, notes, link) }
            } catch (e: Exception) {
                // Không có mạng hoặc GitHub không trả lời: bỏ qua, lần sau kiểm tra lại
            }
        }
    }

    private fun showUpdate(title: String, notes: String, link: String) {
        if (isFinishing || isDestroyed || link.isBlank()) return
        AlertDialog.Builder(this)
            .setTitle("Đã có bản cập nhật")
            .setMessage(if (notes.isBlank()) title else "$title\n\n$notes")
            .setPositiveButton("Tải bản mới") { _, _ -> openExternal(Uri.parse(link)) }
            .setNegativeButton("Để sau", null)
            .show()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        web.saveState(outState)
    }

    override fun onPause() {
        web.onPause()
        super.onPause()
    }

    override fun onResume() {
        super.onResume()
        web.onResume()
    }

    override fun onDestroy() {
        (web.parent as? ViewGroup)?.removeView(web)
        web.destroy()
        super.onDestroy()
    }

    companion object {
        private const val HOST = "appassets.androidplatform.net"
        private const val START_URL = "https://$HOST/assets/www/index.html"
        private const val RELEASE_API = "https://api.github.com/repos/tunaasieunhat/on-luyen-nha-khoa/releases/latest"
        private const val FOLDER = "On Luyen Nha Khoa"
        private val BRAND = Color.rgb(11, 84, 76)
        private val WALL = Color.rgb(238, 247, 243)
    }
}
