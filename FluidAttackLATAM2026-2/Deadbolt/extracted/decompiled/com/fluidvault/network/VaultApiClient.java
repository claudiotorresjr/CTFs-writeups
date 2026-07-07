package com.fluidvault.network;

import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class VaultApiClient {

    private static final String TAG = "VaultApiClient";
    private static final String BASE_URL = BuildConfig.API_BASE_URL;

    public static JSONObject getVaultInfo() throws Exception {
        URL url = new URL(BASE_URL + "/api/vault/info");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");

        BufferedReader reader = new BufferedReader(
            new InputStreamReader(conn.getInputStream())
        );
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        return new JSONObject(sb.toString());
    }

    public static JSONObject submitAdminAuth(
        String masterPassword
    ) throws Exception {
        URL url = new URL(BASE_URL + "/api/vault/admin");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        JSONObject body = new JSONObject();
        body.put("master_password", masterPassword);

        OutputStream os = conn.getOutputStream();
        os.write(body.toString().getBytes(StandardCharsets.UTF_8));
        os.close();

        int status = conn.getResponseCode();
        BufferedReader reader;
        if (status >= 200 && status < 300) {
            reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream())
            );
        } else {
            reader = new BufferedReader(
                new InputStreamReader(conn.getErrorStream())
            );
        }

        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        return new JSONObject(sb.toString());
    }
}
