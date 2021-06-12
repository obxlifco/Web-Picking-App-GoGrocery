//
//  ReplacementViewController.swift
//  GoGrocery
//
//  Created by NAV63 on 24/08/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit
class ReplacementViewController: UIViewController {
//    MARK:- Outlet Declaration
    @IBOutlet weak var viewNavigation: UIView!
    @IBOutlet weak var btnSubmitReplacement: UIButton!
    @IBOutlet weak var btnDontSubmitReplacement: UIButton!
    @IBOutlet weak var repTableView: UITableView!
    
//    MARK:- Variable Declaration
    private let spacing:CGFloat = 1
    override func viewDidLoad() {
        super.viewDidLoad()

        repTableView.delegate = self
        repTableView.dataSource = self
        // Do any additional setup after loading the view.
    }
    override func viewWillAppear(_ animated: Bool) {
        self.navigationController?.isNavigationBarHidden = true
    }
    
    @IBAction func btnBackAction(_ sender: Any) {
          self.navigationController?.popViewController(animated: true)
    }
    
    
    @IBAction func btnSubmitReplacementAction(_ sender: Any) {
    }

}
extension ReplacementViewController : UITableViewDelegate, UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 10
    }
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
          return 350
      }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ReplaceTableViewCell", for: indexPath) as! ReplaceTableViewCell
        return cell
    }
    func tableView(_ tableView: UITableView, willDisplay cell: UITableViewCell, forRowAt indexPath: IndexPath) {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ReplaceTableViewCell") as! ReplaceTableViewCell
        cell.repoCollectionView.dataSource = self
        cell.repoCollectionView.delegate = self
        cell.repoCollectionView.reloadData()

    }

}
extension ReplacementViewController : UICollectionViewDelegate, UICollectionViewDataSource {
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return 10
    }
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "ReplaceCollectionViewCell", for: indexPath) as! ReplaceCollectionViewCell
        cell.backgroundColor = .red
        cell.isHidden = false
        cell.alpha = 1
        return cell
    }
    
    
}
extension ReplacementViewController : UICollectionViewDelegateFlowLayout {
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
//        let numberOfItemsPerRow:CGFloat = 2
//        let spacingBetweenCells:CGFloat = 1
//
//        let totalSpacing = (2 * self.spacing) + ((numberOfItemsPerRow - 1) * spacingBetweenCells) //Amount of total spacing in a row
//
//        if let collection = self.repTableView {
//            let width = (collection.bounds.width - totalSpacing)/numberOfItemsPerRow
//            return CGSize(width: width, height: 320)
//        }
//        else{
//            return CGSize(width: 0, height: 0)
//        }
// */
         return CGSize(width: 180, height: 150)
    }
    
}

