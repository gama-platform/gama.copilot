package gama.ui.copilot;

import org.eclipse.core.runtime.preferences.ConfigurationScope;
import org.osgi.service.prefs.BackingStoreException;

/**
 * Runs before the GAMA workbench starts, without starting the upstream UI bundle.
 */
public final class CopilotStartup implements Runnable {

    @Override
    public void run() {
        var preferences = ConfigurationScope.INSTANCE.getNode("com.microsoft.copilot.eclipse.ui");
        if (preferences.get("copilotQuickStartVersion", null) == null) {
            preferences.putInt("copilotQuickStartVersion", 1);
        }
        if (preferences.get("autoShowWhatsNew", null) == null) {
            preferences.putBoolean("autoShowWhatsNew", false);
        }
        try {
            preferences.flush();
        } catch (BackingStoreException e) {
            throw new IllegalStateException("Cannot save Copilot startup preferences", e);
        }
    }
}
