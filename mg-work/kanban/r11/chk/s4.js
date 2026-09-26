
      // Sync theme with dev workbench if opened from it; default light.
      (function () {
        try {
          var t = localStorage.getItem('giencoder-theme');
          if (t === 'dark' || location.hash === '#dark') document.documentElement.setAttribute('giencoder-theme', 'dark');
        } catch (e) {}
      })();
    