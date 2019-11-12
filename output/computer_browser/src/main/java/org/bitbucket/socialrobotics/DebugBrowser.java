
package org.bitbucket.socialrobotics;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import javax.swing.JFrame;

import org.apache.commons.lang3.StringUtils;

import com.google.gson.Gson;
import com.sun.javafx.webkit.WebConsoleListener;

import javafx.application.Platform;
import javafx.embed.swing.JFXPanel;
import javafx.scene.Scene;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPubSub;

public class DebugBrowser extends JFrame {
	private static final long serialVersionUID = 1L;
	private static final String[] topics = new String[] { "tablet_control", "tablet_image", "tablet_video",
			"tablet_web", "tablet_question_yn", "tablet_question_rate", "tablet_text", "tablet_caption",
			"tablet_overlay", "tablet_input_name", "tablet_input_date", "tablet_input_numbers", "tablet_input_text",
			"tablet_input_multiple", "tablet_stream", "audio_language", "tablet_background", "tablet_config" };
	private final Gson gson = new Gson();
	private final String server;
	private WebEngine engine;
	private String background = "";
	private Object[] components = new Object[0];
	private String language = "en-US";

	public static void main(final String... args) {
		System.setProperty("sun.net.http.allowRestrictedHeaders", "true");
		final String server = (args.length > 0) ? args[0] : "192.168.56.102";
		final DebugBrowser browser = new DebugBrowser(server);
		browser.run();
	}

	public DebugBrowser(final String server) {
		super("CBSR Browser");
		this.server = server;

		final JFXPanel jfxPanel = new JFXPanel();
		WebConsoleListener.setDefaultListener(new WebConsoleListener() {
			@Override
			public void messageAdded(final WebView webView, final String message, final int lineNumber,
					final String sourceId) {
				System.err.println("[" + sourceId + ":" + lineNumber + "] " + message);
			}
		});
		Platform.runLater(new Runnable() {
			@Override
			public void run() {
				final WebView view = new WebView();
				DebugBrowser.this.engine = view.getEngine();
				final Scene scene = new Scene(view);
				jfxPanel.setScene(scene);
			}
		});
		add(jfxPanel);

		setSize(1280, 800);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setVisible(true);
	}

	public void run() {
		try (final Jedis redis = new Jedis(this.server)) {
			System.out.println("Subscribing to " + this.server);
			redis.subscribe(new JedisPubSub() {
				@Override
				public void onMessage(final String channel, final String message) {
					switch (channel) {
					case "tablet_control":
						if (message.equals("reload")) {
							load(null);
						} // ignore hide & show?
						break;
					case "tablet_image":
						load(getURL("img", message));
						break;
					case "tablet_video":
						load(getURL("video", message));
						break;
					case "tablet_web":
						load(message);
						break;
					case "tablet_question_yn":
						load(getURL("question_yn", message));
						break;
					case "tablet_question_rate":
						load(getURL("question_rate", message.split(";")));
						break;
					case "tablet_text":
						load(getURL("text", message));
						break;
					case "tablet_caption":
						load(getURL("caption", message.split(";")));
						break;
					case "tablet_overlay":
						load(getURL("overlay", message.split(";")));
						break;
					case "tablet_input_name":
						load(getURL("input_name", message));
						break;
					case "tablet_input_date":
						load(getURL("input_date", message));
						break;
					case "tablet_input_numbers":
						load(getURL("input_numbers", message.split(";")));
						break;
					case "tablet_input_text":
						load(getURL("input_text", message));
						break;
					case "tablet_input_multiple":
						load(getURL("input_multiple", message.split(";")));
						break;
					case "tablet_stream":
						load(getURL("stream"));
						break;
					case "audio_language":
						DebugBrowser.this.language = message;
						break;
					case "tablet_background":
						DebugBrowser.this.background = message;
						break;
					case "tablet_config":
						final String[] split = message.split(";");
						DebugBrowser.this.components = new Object[split.length];
						for (int i = 0; i < split.length; i++) {
							final String[] parts = split[i].split(",");
							final Map<String, Object> result = new LinkedHashMap<>(parts.length);
							result.put("build", parts[0]);
							result.put("position", parts[1]);
							final Map<String, String> args = new LinkedHashMap<>(parts.length - 2);
							for (int j = 2; j < parts.length; j++) {
								final String[] arg = parts[j].split("=");
								args.put(arg[0], arg[1]);
							}
							result.put("args", args);
							DebugBrowser.this.components[i] = result;
						}
						break;
					}
				}
			}, topics);
		}
	}

	private void load(final String url) {
		Platform.runLater(new Runnable() {
			@Override
			public void run() {
				if (url == null) {
					System.out.println("Reloading...");
					DebugBrowser.this.engine.reload();
				} else {
					System.out.println("Loading " + url);
					DebugBrowser.this.engine.load(url);
				}
			}
		});
	}

	private String getURL(final String type, final String... content) {
		final String base = "http://" + this.server + ":8000/";
		final String index = base + "index.html?view=";
		switch (type) {
		case "img":
		case "video":
			return base + type + "/" + content[0];
		case "question_yn":
		case "input_date":
		case "input_text":
			return index + type + "&q=" + encode(content[0]) + baseParams();
		case "question_rate":
			return index + type + "&scale=" + content[0] + "&q=" + encode(content[1]) + baseParams();
		case "text":
			return index + type + "&text=" + encode(content[0]) + baseParams();
		case "caption":
			final String imgURL = getURL("img", content[0]);
			return index + type + "&image_src=" + encode(imgURL) + "&caption=" + encode(content[1]) + baseParams();
		case "overlay":
			final String img1URL = getURL("img", content[0]);
			final String img2URL = getURL("img", content[1]);
			return index + type + "&image_src=" + encode(img1URL) + "&overlay_src=" + encode(img2URL) + baseParams();
		case "input_name":
			return index + type + "&name=" + encode(content[0]) + baseParams();
		case "input_numbers":
			return index + type + "&digits=" + content[0] + "&q=" + encode(content[1]) + baseParams();
		case "input_multiple":
			final String question = encode(content[0]);
			final List<String> answers = new LinkedList<>();
			for (int i = 1; i < content.length; ++i) {
				answers.add(content[i]);
			}
			return index + type + "&q=" + question + "&n=" + answers.size() + "&options="
					+ encode(StringUtils.join(answers, ";")) + baseParams();
		case "stream":
			return index + type;
		default:
			throw new IllegalArgumentException("unknown type " + type);
		}
	}

	private String baseParams() {
		return "&bg=" + encode(this.background) + "&components=" + encode(this.gson.toJson(this.components)) + "&lang="
				+ encode(this.language);
	}

	private static String encode(final String string) {
		try {
			return URLEncoder.encode(string, "UTF-8").replaceAll("\\+", "%20");
		} catch (final UnsupportedEncodingException e) {
			return string;
		}
	}
}
