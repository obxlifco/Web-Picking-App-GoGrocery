//
//  subMenuViewController.swift
//  SlideInTransition
//
//  Created by jay's on 17/12/19.
//  Copyright © 2019 jay's. All rights reserved.
//

import UIKit
class subMenuViewController: UIViewController {

    @IBOutlet weak var tableVIew: UITableView!
    var submenulist = [String : Any]()
    let transiton = SlideInTransition()
    
    var numberofsubcellarr = [String]()
    
    @IBOutlet weak var TitleName: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
 
        TitleName.text = submenulist["title"] as! String
        numberofsubcellarr = submenulist["numberofsubcell"] as! [String]
        

    }
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.setNavigationBarHidden(true, animated: animated)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        navigationController?.setNavigationBarHidden(false, animated: animated)
    }
 
    @IBAction func BackAction(_ sender: Any) {
        
                guard let menuViewController = storyboard?.instantiateViewController(withIdentifier: "MenuViewController") as? MenuViewController else { return }
//             menuViewController.didTapMenuType = { menuType in
//                 self.transitionToNew(menuType)
//             }
             menuViewController.modalPresentationStyle = .overCurrentContext
             menuViewController.transitioningDelegate = self
             present(menuViewController, animated: true)
      //  navigationController?.popToRootViewController(animated: true)
    }
    
    
}
//MARK : - UITableViewDelegate
extension subMenuViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
            return self.numberofsubcellarr.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell { let adsCell = tableView.dequeueReusableCell(withIdentifier: "cellsub") as! cellsub
        adsCell.textLabel?.text = numberofsubcellarr[indexPath.row]
        
        return adsCell
    }
     
}
class cellsub: UITableViewCell
{
    
}
extension subMenuViewController: UIViewControllerTransitioningDelegate {
    func animationController(forPresented presented: UIViewController, presenting: UIViewController, source: UIViewController) -> UIViewControllerAnimatedTransitioning? {
        transiton.isPresenting = true
        return transiton
    }

    func animationController(forDismissed dismissed: UIViewController) -> UIViewControllerAnimatedTransitioning? {
        transiton.isPresenting = false
        return transiton
    }
}
