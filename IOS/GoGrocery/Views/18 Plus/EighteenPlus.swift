//
//  EighteenPlus.swift
//  GoGrocery
//
//  Created by NAV63 on 11/06/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class EighteenPlus: UIView {
    @IBOutlet weak var viewEighteen: UIView!
    
    @IBOutlet weak var lblText: UILabel!
    @IBOutlet weak var btnAboveAge: UIButton!
    @IBOutlet weak var btnBelowAge: UIButton!
    
}
var AgeCheckView = EighteenPlus()
func requestAgeCheckView(vc: UIViewController){
    
    AgeCheckView.removeFromSuperview() // make it only once
    AgeCheckView = Bundle.main.loadNibNamed("EighteenPlus", owner: vc, options: nil)?.first as! EighteenPlus
    AgeCheckView.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    AgeCheckView.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        AgeCheckView.alpha = 1
    }
    appdelegate.window?.addSubview(AgeCheckView)
}
