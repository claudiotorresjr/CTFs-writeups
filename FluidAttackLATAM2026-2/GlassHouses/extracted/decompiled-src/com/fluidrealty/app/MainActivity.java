package com.fluidrealty.app;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.fluidrealty.app.adapter.PropertyAdapter;
import com.fluidrealty.app.model.Property;
import com.fluidrealty.app.network.ApiClient;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "FluidRealty";
    private RecyclerView propertyList;
    private PropertyAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        propertyList = findViewById(R.id.property_list);
        propertyList.setLayoutManager(new LinearLayoutManager(this));

        loadProperties();
        handleDeepLink(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        handleDeepLink(intent);
    }

    private void handleDeepLink(Intent intent) {
        if (intent == null || intent.getData() == null) {
            return;
        }

        Uri deepLink = intent.getData();
        String scheme = deepLink.getScheme();

        if (!"fluidrealty".equals(scheme)) {
            return;
        }

        String action = deepLink.getHost();
        Log.d(TAG, "Deep link received: " + deepLink.toString());

        switch (action) {
            case "view":
                String url = deepLink.getQueryParameter("url");
                if (url != null) {
                    Intent webViewIntent = new Intent(this, WebViewActivity.class);
                    webViewIntent.putExtra("load_url", url);
                    startActivity(webViewIntent);
                }
                break;

            case "property":
                String propertyId = deepLink.getQueryParameter("id");
                if (propertyId != null) {
                    openPropertyDetail(Integer.parseInt(propertyId));
                }
                break;

            case "search":
                String query = deepLink.getQueryParameter("q");
                if (query != null) {
                    searchProperties(query);
                }
                break;

            default:
                Log.w(TAG, "Unknown deep link action: " + action);
                break;
        }
    }

    private void loadProperties() {
        ApiClient.getInstance().getProperties(new ApiClient.Callback<List<Property>>() {
            @Override
            public void onSuccess(List<Property> properties) {
                adapter = new PropertyAdapter(properties);
                propertyList.setAdapter(adapter);
            }

            @Override
            public void onError(String error) {
                Log.e(TAG, "Failed to load properties: " + error);
            }
        });
    }

    private void openPropertyDetail(int id) {
        Intent intent = new Intent(this, PropertyDetailActivity.class);
        intent.putExtra("property_id", id);
        startActivity(intent);
    }

    private void searchProperties(String query) {
        Log.d(TAG, "Searching for: " + query);
    }
}
