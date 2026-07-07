package com.fluidrealty.app.network;

import com.fluidrealty.app.model.Property;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Query;

public interface ApiService {

    @GET("/api/properties")
    Call<List<Property>> getProperties();

    @GET("/api/properties")
    Call<List<Property>> getPropertiesByCity(@Query("city") String city);

    @GET("/api/properties/admin")
    Call<List<Property>> getAdminProperties(
        @Header("Authorization") String authorization
    );
}
