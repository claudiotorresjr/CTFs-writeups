package com.whisperchat.app.data;

import java.io.IOException;

import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/* Builds the Retrofit client and attaches the API key to every request. */
public final class ApiClient {
    private static final String BASE_URL = "https://api.whisperchat.internal";
    private static final String API_KEY = "fluidctf-api-2026-whispers";

    private static WhisperApi service;

    public static WhisperApi get() {
        if (service == null) {
            OkHttpClient http = new OkHttpClient.Builder()
                    .addInterceptor(new Interceptor() {
                        @Override
                        public Response intercept(Chain chain) throws IOException {
                            Request request = chain.request().newBuilder()
                                    .header("X-API-Key", API_KEY)
                                    .header("User-Agent", "WhisperChat/1.4.2 (Android 14; SDK 34)")
                                    .build();
                            return chain.proceed(request);
                        }
                    })
                    .build();
            service = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(http)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build()
                    .create(WhisperApi.class);
        }
        return service;
    }
}
