// SPDX-License-Identifier: GPL-3.0-or-later
// Mango Port's Home Screen launcher: a tiny app that opens one game in Mango Port.
//
// Built once (scripts/build-launcher.sh, run by Madeira's tools/build/package-ipa.sh through
// patch 0018) and shipped inside Mango Port as MangoLauncher.b64. Mango Port's "Make Home Screen
// app" copies it into a new IPA with the game's name, icon and its link in Info.plist
// (MangoLaunchURL); Mango Signer signs and installs that IPA. Opening it opens the link.

import UIKit

final class LaunchController: UIViewController {
    private let label = UILabel()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 0.08, green: 0.05, blue: 0.03, alpha: 1)
        label.textColor = .white
        label.numberOfLines = 0
        label.textAlignment = .center
        label.font = .systemFont(ofSize: 17, weight: .semibold)
        label.text = "Opening in Mango Port…"
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)
        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            label.leadingAnchor.constraint(greaterThanOrEqualTo: view.leadingAnchor, constant: 24),
        ])
    }

    func openGame() {
        guard let text = Bundle.main.object(forInfoDictionaryKey: "MangoLaunchURL") as? String,
              let url = URL(string: text) else {
            label.text = "This launcher has no game set."
            return
        }
        label.text = "Opening in Mango Port…"
        UIApplication.shared.open(url, options: [:]) { [weak self] opened in
            if !opened { self?.label.text = "Install Mango Port to play this game." }
        }
    }
}

@objc(MangoSceneDelegate)
final class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    private let controller = LaunchController()

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let window = UIWindow(windowScene: windowScene)
        window.rootViewController = controller
        window.makeKeyAndVisible()
        self.window = window
    }

    func sceneDidBecomeActive(_ scene: UIScene) {
        controller.openGame()
    }
}

@main
final class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication,
                     configurationForConnecting connectingSceneSession: UISceneSession,
                     options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        let configuration = UISceneConfiguration(name: "Default", sessionRole: connectingSceneSession.role)
        configuration.delegateClass = SceneDelegate.self
        return configuration
    }
}
