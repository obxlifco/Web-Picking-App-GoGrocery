import UIKit
class AppUpdate: UIView {
    @IBOutlet weak var updateView: UIView!
    @IBOutlet weak var btnUpgrade: UIButton!
    @IBOutlet weak var imgImage: UIImageView!
    
}
var appUpdateTypeViewXib = AppUpdate()
func requestAppUpdateGlobal(){
    
    appUpdateTypeViewXib.removeFromSuperview() // make it only once
    appUpdateTypeViewXib = Bundle.main.loadNibNamed("AppUpdate", owner: nil, options: nil)?.first as! AppUpdate
    appUpdateTypeViewXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    appUpdateTypeViewXib.alpha = 0
    UIView.animate(withDuration: 0.5) {
        appUpdateTypeViewXib.alpha = 1
    }
    appdelegate.window?.addSubview(appUpdateTypeViewXib)
}
