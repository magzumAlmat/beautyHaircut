#!/usr/bin/env python3
"""
Hair Style Selector API Server (Simple HTTP Server)
Запуск через: python server.py

Этот сервер работает как альтернатива backend.py на FastAPI.
Он использует Pillow для процедурной генерации пепельных волос.
"""

import http.server
import socketserver
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import base64
import os
import io
from datetime import datetime, timezone


# ─── Конфигурация ──────────────────────────────
HOST = "127.0.0.1"
PORT = 8001
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLES_DATA = {
    "hollywood": {"name": "Голливудские волны", "category": "вечерние"},
    "high_bun": {"name": "Высокий текстурный пучок", "category": "вечерние"},
    "low_bun": {"name": "Низкий гладкий пучок", "category": "вечерние"},
    "greek_braid": {"name": "Греческая коса", "category": "вечерние"},
    "french_twist": {"name": "Французский твист (ракушка)", "category": "вечерние"},
    "blowout": {"name": "Брашинг-объем", "category": "салонные"},
    "beach_waves": {"name": "Пляжные волны (Beach Waves)", "category": "салонные"},
    "wet_hair": {"name": "Эффект «влажных волос»", "category": "салонные"},
    "high_ponytail": {"name": "Высокий текстурный хвост", "category": "салонные"},
    "pearl_bun": {"name": "Пудровый пучок (Pearl Bun)", "category": "салонные"},
    "bob": {"name": "Каре / Боб-каре", "category": "стрижки"},
    "cascade": {"name": "Каскад и Лесенка", "category": "стрижки"},
    "pixie": {"name": "Пикси", "category": "стрижки"},
    "wolfcut": {"name": "Вулфкат (Wolfcut) / Шегги", "category": "стрижки"},
}

HAIR_COLORS = {
    "ash_gray":       (168, 169, 173),   # пепельный серый
    "light_ash":      (192, 192, 200),   # светло-пепельный
    "dark_gray":      (112, 112, 112),   # тёмно-серый
    "platinum":       (225, 230, 235),   # платиновый блонд
}


# ─── HTTP Handler ──────────────────────────────
class Handler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "service": "Hair Style Selector API (Pillow Fallback)",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }).encode())
            return
        
        elif parsed.path == "/api/styles":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            styles = [{"id": k, **v} for k, v in STYLES_DATA.items()]
            self.wfile.write(json.dumps(styles).encode())
            return
        
        elif parsed.path.startswith("/api/download/"):
            filename = parsed.path[len("/api/download/"):]
            filepath = OUTPUT_DIR / filename
            if filepath.exists():
                with open(filepath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404, "Файл не найден")
            return
        
        elif parsed.path == "/":
            # Главная страница с инструкцией
            html = """<!DOCTYPE html>
<html><head><title>Hair Style Selector API</title></head>
<body style="font-family:sans-serif;padding:2rem;background:#1a1a2e;color:#eee;">
<h1>🎨 Hair Style Selector API</h1>
<p><code>http://localhost:8001</code></p>
<h3>Endpoints:</h3>
<ul>
<li><code>GET  /health</code> — статус сервера</li>
<li><code>GET  /api/styles</code> — список причесок</li>
<li><code>POST /api/generate</code> — генерация (form-data)</li>
</ul>
<h3>Пример запроса:</h3>
<pre>curl -X POST http://localhost:8001/api/generate \\
  -F "image=@photo.jpg" \\
  -F "style_id=bob" \\
  -F "color=ash_gray"</pre>
<p style="margin-top:2rem;color:#666;font-size:.9rem;">
Powered by Pillow • 14 причесок • Пепельный цвет волос
</p>
</body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return
        
        else:
            # Статический контент (frontend) — для простоты не используем здесь
            self.send_error(404, "Not Found")
            return
    
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        
        parsed = urlparse(self.path)
        
        # POST /api/generate
        if parsed.path == "/api/generate":
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
            except:
                self.send_error(400, "Неверный JSON body. Ожидается: {\"image\": \"base64...\", \"style_id\": \"bob\"}")
                return
            
            image_url = data.get("image", "")
            style_id = data.get("style_id", "bob")
            
            # Декодируем base64 изображение
            if "," in image_url:
                _, encoded = image_url.split(",", 1)
                try:
                    img_bytes = base64.b64decode(encoded)
                except Exception as e:
                    self.send_error(400, f"Ошибка декодирования base64: {e}")
                    return
            else:
                # Если URL — считаем это как файл (для тестов можно использовать base64 напрямую)
                try:
                    img_bytes = base64.b64decode(image_url)
                except Exception as e:
                    self.send_error(400, f"Неверный формат image. Ошибка: {e}")
                    return
            
            style = STYLES_DATA.get(style_id, {"name": style_id})
            
            # Применяем стилизацию волос (Pillow)
            img_data = self._apply_hair_style(img_bytes, style_id)
            
            if img_data is None:
                self.send_error(500, "Ошибка обработки изображения")
                return
            
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"{style_id}_{timestamp}.png"
            output_path = OUTPUT_DIR / filename
            
            with open(output_path, "wb") as f:
                f.write(img_data)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            result = {
                "success": True,
                "style_id": style_id,
                "style_name": style["name"],
                "color": "ash_gray",
                "result_url": f"/api/download/{filename}",
                "output_path": str(output_path),
            }
            self.wfile.write(json.dumps(result).encode())
            return
        
        self.send_error(404, "Unknown endpoint")
    
    def _apply_hair_style(self, img_bytes: bytes, style_id: str) -> bytes | None:
        """Применяет стилизацию волос к изображению с помощью Pillow."""
        
        try:
            from PIL import Image
            
            # Декодируем PNG
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            
            w, h = img.size
            
            # Создаём маску области волос (верхняя часть изображения)
            result = img.copy()
            
            for y in range(h):
                for x in range(w):
                    r, g, b = img.getpixel((x, y))
                    
                    # Волосы обычно занимают верхнюю ~60% высоты
                    if 0.15 < y / h < 0.7:
                        brightness = (r + g + b) / 3
                        
                        # Тёмные области — это волосы
                        if brightness < 160:
                            # Применяем пепельный цвет волос
                            base_color = HAIR_COLORS["ash_gray"]
                            
                            # Добавляем текстуру (шум для реалистичности)
                            noise_r = int((x / w - 0.5) * 8) + int((y / h - 0.5) * 4)
                            noise_g = int((x % 9 - 4) * 2) + int((y % 6 - 3))
                            noise_b = int((y / h - 0.5) * 8) + int((x % 7 - 3) * 2)
                            
                            new_r = max(0, min(255, base_color[0] + noise_r))
                            new_g = max(0, min(255, base_color[1] + noise_g))
                            new_b = max(0, min(255, base_color[2] + noise_b))
                            
                            result.putpixel((x, y), (new_r, new_g, new_b))
                        else:
                            # Светлые области — кожа, оставляем без изменений
                            pass
            
            img_byte_arr = io.BytesIO()
            result.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
            
        except ImportError as e:
            print(f"⚠️ Pillow не установлен: {e}")
            self.send_error(500, "Pillow не установлен. Установите: pip install Pillow")
            return None
        except Exception as e:
            print(f"❌ Ошибка в _apply_hair_style: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return None


# ─── Запуск сервера ──────────────────────────────
if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"\n{'='*50}")
        print("🚀 Hair Style Selector API Server (Pillow Fallback)")
        print(f"   📡 API:      http://{HOST}:{PORT}/health")
        print(f"   🎨 Frontend: http://localhost:3000  (React Vite)")
        print(f"   📁 Outputs:  {OUTPUT_DIR.absolute()}")
        print("="*50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Сервер остановлен.")
