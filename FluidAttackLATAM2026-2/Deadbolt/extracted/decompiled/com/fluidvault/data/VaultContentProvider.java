package com.fluidvault.data;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.text.TextUtils;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

public class VaultContentProvider extends ContentProvider {

    private static final String AUTHORITY = "com.fluidvault.app.provider";
    private static final String TABLE_ENTRIES = "vault_entries";
    private static final int ENTRIES = 1;
    private static final int ENTRY_ID = 2;

    private static final UriMatcher uriMatcher = new UriMatcher(
        UriMatcher.NO_MATCH
    );

    static {
        uriMatcher.addURI(AUTHORITY, "entries", ENTRIES);
        uriMatcher.addURI(AUTHORITY, "entries/#", ENTRY_ID);
    }

    private VaultDatabaseHelper dbHelper;

    @Override
    public boolean onCreate() {
        dbHelper = new VaultDatabaseHelper(getContext());
        return true;
    }

    @Nullable
    @Override
    public Cursor query(
        @NonNull Uri uri,
        @Nullable String[] projection,
        @Nullable String selection,
        @Nullable String[] selectionArgs,
        @Nullable String sortOrder
    ) {
        SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
        qb.setTables(TABLE_ENTRIES);
        qb.setStrict(true);

        switch (uriMatcher.match(uri)) {
            case ENTRIES:
                break;
            case ENTRY_ID:
                qb.appendWhere("_id = ?");
                selectionArgs = new String[]{ uri.getLastPathSegment() };
                break;
            default:
                throw new IllegalArgumentException("Unknown URI: " + uri);
        }

        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Cursor cursor = qb.query(
            db, projection, selection, selectionArgs,
            null, null,
            TextUtils.isEmpty(sortOrder) ? "_id ASC" : sortOrder
        );
        cursor.setNotificationUri(getContext().getContentResolver(), uri);
        return cursor;
    }

    @Nullable
    @Override
    public String getType(@NonNull Uri uri) {
        switch (uriMatcher.match(uri)) {
            case ENTRIES:
                return "vnd.android.cursor.dir/vnd.fluidvault.entry";
            case ENTRY_ID:
                return "vnd.android.cursor.item/vnd.fluidvault.entry";
            default:
                throw new IllegalArgumentException("Unknown URI: " + uri);
        }
    }

    @Nullable
    @Override
    public Uri insert(
        @NonNull Uri uri,
        @Nullable ContentValues values
    ) {
        if (uriMatcher.match(uri) != ENTRIES) {
            throw new IllegalArgumentException(
                "Insert not supported for URI: " + uri
            );
        }
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        long id = db.insertOrThrow(TABLE_ENTRIES, null, values);
        getContext().getContentResolver().notifyChange(uri, null);
        return Uri.withAppendedPath(uri, String.valueOf(id));
    }

    @Override
    public int delete(
        @NonNull Uri uri,
        @Nullable String selection,
        @Nullable String[] selectionArgs
    ) {
        throw new UnsupportedOperationException(
            "Delete not permitted on vault entries"
        );
    }

    @Override
    public int update(
        @NonNull Uri uri,
        @Nullable ContentValues values,
        @Nullable String selection,
        @Nullable String[] selectionArgs
    ) {
        if (uriMatcher.match(uri) != ENTRY_ID) {
            throw new IllegalArgumentException(
                "Update requires specific entry URI"
            );
        }
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        int rows = db.update(
            TABLE_ENTRIES, values,
            "_id = ?",
            new String[]{ uri.getLastPathSegment() }
        );
        if (rows > 0) {
            getContext().getContentResolver().notifyChange(uri, null);
        }
        return rows;
    }
}
