package hackathon.pro.kabaddi;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.net.URL;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

/**
 * Main Application to read data from JSON file through website URL
 *
 */
public class MainApp {
	public static String teamUrl;
	public static String matchUrl;

	public static void main(String[] args) { // JSON parser object to parse read file
		JSONParser jsonParser = new JSONParser();
		try {
			init();
			String standing = readUrl(KabaddiContants.BASE_URL + KabaddiContants.ALL_STATNDING);

			// Read JSON file as clientConfigObject
			JSONObject clientConfigObject = (JSONObject) jsonParser.parse(standing);
			// Get config object within list
			JSONObject standings = (JSONObject) clientConfigObject.get("standings");
			// Get kabaddiPaths object within list
			JSONArray groups = (JSONArray) standings.get("groups");

			groups.forEach(group -> {
				final JSONObject teams = (JSONObject) ((JSONObject) group).get("teams");
				final JSONArray team = (JSONArray) teams.get("team");
				team.forEach(teamItr -> {
					final Long teamId = (Long) ((JSONObject) teamItr).get("team_id");
					try {
						final String teamData = readUrl(
								KabaddiContants.BASE_URL + teamUrl.replace("{{team_Id}}", String.valueOf(teamId)));
						final FileOutputStream outputStreamTeam = new FileOutputStream(
								"/home/ash/AI_AND_ML/Artificial-Intelligence/Hackathon - Pro Kabaddi League/pro-kabaddi-data-extractor/data/"
										+ teamId + "_player.json");
						outputStreamTeam.write(teamData.getBytes());
						System.out.println(teamId + "_player.json");
						final JSONObject matchResult = (JSONObject) ((JSONObject) teamItr).get("match_result");
						final JSONArray matchs = (JSONArray) matchResult.get("match");
						matchs.forEach(match -> {
							final Long matchId = (Long) ((JSONObject) match).get("id");
							try {
								final String matchData = readUrl(KabaddiContants.BASE_URL
										+ matchUrl.replace("{{MATCH_ID}}", String.valueOf(matchId)));
								final FileOutputStream outputStreamMatch = new FileOutputStream(
										"/home/ash/AI_AND_ML/Artificial-Intelligence/Hackathon - Pro Kabaddi League/pro-kabaddi-data-extractor/data/"
												+ matchId + "_match.json");
								outputStreamMatch.write(matchData.getBytes());
								System.out.println(matchId + "_match.json");
							} catch (final Exception e) {
								e.printStackTrace();
							}
						});
					} catch (final Exception e) {
						e.printStackTrace();
					}
				});
			});
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static void init() {
		initTeamURL();
	}

	private static void initTeamURL() {
		JSONParser jsonParser = new JSONParser();
		try {
			String clientConfig = readUrl(KabaddiContants.BASE_URL + KabaddiContants.CLIENT_CONIFG);

			// Read JSON file as clientConfigObject
			JSONObject clientConfigObject = (JSONObject) jsonParser.parse(clientConfig);

			// Get config object within list
			JSONObject config = (JSONObject) clientConfigObject.get("config");

			// Get kabaddiPaths object within list
			JSONObject kabaddiPaths = (JSONObject) config.get("kabaddiPaths");

			// Get kabaddiPaths object within list
			teamUrl = (String) kabaddiPaths.get("teamstats");

			// Get kabaddiPaths object within list
			matchUrl = (String) kabaddiPaths.get("matchFile");
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	private static String readUrl(String urlString) throws Exception {
		BufferedReader reader = null;
		try {
			URL url = new URL(urlString);
			reader = new BufferedReader(new InputStreamReader(url.openStream()));
			StringBuffer buffer = new StringBuffer();
			int read;
			char[] chars = new char[1024];
			while ((read = reader.read(chars)) != -1)
				buffer.append(chars, 0, read);

			return buffer.toString();
		} finally {
			if (reader != null)
				reader.close();
		}
	}
}