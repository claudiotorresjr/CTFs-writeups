package com.fluidrealty.app.network;

import android.util.Log;

import com.fluidrealty.app.model.Property;

import java.io.IOException;
import java.util.List;

import okhttp3.Interceptor;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ApiClient {

    private static final String TAG = "FluidRealty.API";
    private static final String BASE_URL = "https://api.fluidrealty.co/";
    private static ApiClient instance;
    private final ApiService apiService;

    private ApiClient() {
        OkHttpClient client = new OkHttpClient.Builder()
            .addInterceptor(new Interceptor() {
                @Override
                public Response intercept(Chain chain) throws IOException {
                    Request original = chain.request();
                    Request request = original.newBuilder()
                        .header("X-App-Version", "3.7.2")
                        .header("X-Platform", "android")
                        .method(original.method(), original.body())
                        .build();
                    return chain.proceed(request);
                }
            })
            .build();

        Retrofit retrofit = new Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build();

        apiService = retrofit.create(ApiService.class);
    }

    public static synchronized ApiClient getInstance() {
        if (instance == null) {
            instance = new ApiClient();
        }
        return instance;
    }

    public void getProperties(Callback<List<Property>> callback) {
        apiService.getProperties().enqueue(new retrofit2.Callback<List<Property>>() {
            @Override
            public void onResponse(Call<List<Property>> call,
                                   retrofit2.Response<List<Property>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    callback.onSuccess(response.body());
                } else {
                    callback.onError("API error: " + response.code());
                }
            }

            @Override
            public void onFailure(Call<List<Property>> call, Throwable t) {
                Log.e(TAG, "Request failed", t);
                callback.onError(t.getMessage());
            }
        });
    }

    public void getAdminProperties(String authToken,
                                    Callback<List<Property>> callback) {
        apiService.getAdminProperties("Bearer " + authToken)
            .enqueue(new retrofit2.Callback<List<Property>>() {
                @Override
                public void onResponse(Call<List<Property>> call,
                                       retrofit2.Response<List<Property>> response) {
                    if (response.isSuccessful() && response.body() != null) {
                        callback.onSuccess(response.body());
                    } else {
                        callback.onError("Admin API error: " + response.code());
                    }
                }

                @Override
                public void onFailure(Call<List<Property>> call, Throwable t) {
                    Log.e(TAG, "Admin request failed", t);
                    callback.onError(t.getMessage());
                }
            });
    }

    public interface Callback<T> {
        void onSuccess(T result);
        void onError(String error);
    }
}
