//
//  PaymentFailedViewController.swift
//  GoGrocery
//
//  Created by Nav63 on 19/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class PaymentFailedViewController: UIViewController {

    @IBOutlet weak var btnRetry: UIButton!
    override func viewDidLoad() {
        super.viewDidLoad()

        self.btnRetry.layer.cornerRadius = 5
        self.btnRetry.addShadow1()
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    @IBAction func btnRetryAction(_ sender: Any) {
//        let vc = self.storyboard?.instantiateViewController(withIdentifier: "PaymentFailedViewController") as! PaymentFailedViewController
        let storyboard:UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "HomeViewController") as! HomeViewController
        self.navigationController?.pushViewController(vc, animated: true)
//         let navigationController = UINavigationController(rootViewController: vc)
//          let appdelegate = UIApplication.shared.delegate as! AppDelegate
//         appdelegate.window!.rootViewController = navigationController
    }
}
