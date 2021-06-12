//
//  GenderSelection.swift
//  GoGrocery
//
//  Created by BMS-09-M on 02/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class GenderSelection: UIView {

    @IBOutlet weak var btnMale: UIButton!
    @IBOutlet weak var btnMaleFull: UIButton!
    
    @IBOutlet weak var btnFemale: UIButton!
    @IBOutlet weak var btnFemaleFull: UIButton!
    
    @IBOutlet weak var btnOther: UIButton!
    @IBOutlet weak var btnOtherFull: UIButton!
    
    @IBOutlet weak var genderView: UIView!
    @IBOutlet weak var btnApply: UIButton!
    @IBOutlet weak var btnCancel: UIButton!
}

var userTypeViewXib1 = GenderSelection()
func requestViewGlobal1(vc: UIViewController){
    
    userTypeViewXib1.removeFromSuperview() // make it only once
    userTypeViewXib1 = Bundle.main.loadNibNamed("GenderSelection", owner: vc, options: nil)?.first as! GenderSelection
    userTypeViewXib1.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    userTypeViewXib1.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        userTypeViewXib1.alpha = 1
    }
    appdelegate.window?.addSubview(userTypeViewXib1)
}
