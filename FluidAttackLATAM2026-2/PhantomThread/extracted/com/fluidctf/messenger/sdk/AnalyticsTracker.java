package com.fluidctf.messenger.sdk;

import android.content.Context;
import android.util.Log;
import java.util.HashMap;
import java.util.Map;

public class AnalyticsTracker {
    private static final String TAG = "AnalyticsSDK";
    private static AnalyticsTracker instance;
    private final Map<String, Integer> eventCounts;
    private boolean initialized;

    private AnalyticsTracker() {
        this.eventCounts = new HashMap<>();
        this.initialized = false;
    }

    public static synchronized AnalyticsTracker getInstance() {
        if (instance == null) {
            instance = new AnalyticsTracker();
        }
        return instance;
    }

    public void initialize(Context context, String apiKey) {
        if (this.initialized) {
            Log.w(TAG, "AnalyticsTracker already initialized");
            return;
        }
        this.initialized = true;
        Log.d(TAG, "AnalyticsTracker initialized");
    }

    public void logEvent(String eventName) {
        if (!this.initialized) {
            Log.w(TAG, "AnalyticsTracker not initialized, dropping event: " + eventName);
            return;
        }
        Integer count = this.eventCounts.getOrDefault(eventName, 0);
        this.eventCounts.put(eventName, count + 1);
        Log.d(TAG, "Event logged: " + eventName + " (count=" + (count + 1) + ")");
    }

    public void logEvent(String eventName, Map<String, String> params) {
        logEvent(eventName);
    }
}
