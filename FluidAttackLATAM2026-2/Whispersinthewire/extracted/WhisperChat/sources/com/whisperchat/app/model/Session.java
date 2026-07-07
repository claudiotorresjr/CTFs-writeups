package com.whisperchat.app.model;

/* Client-side session state. The isAdmin() flag only toggles UI; the server
 * does not consult it, which is the whole problem. */
public class Session {
    private static final Session CURRENT = new Session();

    private boolean admin = false;

    public static Session current() {
        return CURRENT;
    }

    public boolean isAdmin() {
        return this.admin;
    }
}
