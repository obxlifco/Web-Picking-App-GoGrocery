//
//  EditDeleteXibView.swift
//  GoGrocery
//
//  Created by BMS-09-M on 29/01/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class EditDeleteXibView: UIView {
    @IBOutlet weak var btnEdit: UIButton!
    @IBOutlet weak var btnDelete: UIButton!
    @IBOutlet weak var viewww: UIView!
    @IBOutlet weak var viewEdit: UIView!
    @IBOutlet weak var viewDelete: UIView!
    /*
    // Only override draw() if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func draw(_ rect: CGRect) {
        // Drawing code
    }
    */

}
var EditDeleteXib = EditDeleteXibView()
func requestEditDeleteViewGlobal(vc: UIViewController , yPosition :CGFloat, xPoaition : CGFloat){
    
    EditDeleteXib.removeFromSuperview() // make it only once
    EditDeleteXib = Bundle.main.loadNibNamed("EditDeleteView", owner: vc, options: nil)?.first as! EditDeleteXibView
    EditDeleteXib.frame = CGRect(x:xPoaition, y: yPosition, width: 150, height: 86)
   // EditDeleteXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        EditDeleteXib.alpha = 1
    }
    appdelegate.window?.addSubview(EditDeleteXib)
}

