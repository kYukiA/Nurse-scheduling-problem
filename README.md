# ナーススケジューリング問題　勤務表を自動生成したい
vcopt を使ったpythonプログラムです。自動的に勤務表を生成するプログラムを作成しました。pythonの勉強もかねて作ったプログラムなので間違いがあるかもしれません。
vcopt はビネクラのソフトウェアです(https://vigne-cla.com/)。


## 目的
* 勤務表の作成には時間がかかり、面倒です。
* 制限事項が多く、確認に時間がかかります。
* 負担は特定の人に集中しています。

これらの勤務表作成時の問題を改善したいです。


## 例題の要件
### 前提条件
* 従業員は5人
* 従業員は、勤務表作成前に休み希望を提出します。

### 勤務表の制約
* 3、4人は出勤しなければなりません。
* 従業員間で、土日祝日と重なる休日が同じになるようにしたい。
* 休暇の数を従業員間で揃えたい。
* 指定された2名のうち1名が出勤しなければなりません。

---

# Nurse-scheduling-problem
This is a python program using vcopt. I created a program that automatically generates a work schedule. I made this program to learn python, so there may be some mistakes in it.  vcopt is a software from Vinekula (https://vigne-cla.com/).


## Objective
* Creating a work schedule is time consuming and burdensome.
* There are many restrictions and it takes time to check.
* The burden is concentrated on specific people.

I want to solve these problems.


## Example Requirement
### Prerequisites
* Five employees.
* Employees are required to submit their vacation requests for a few days before they are scheduled to work.

### Work Schedule Restrictions
* Three or four people have to come to work.
* I want to make sure that the number of days off that overlap with weekends and holidays are the same among employees.
* I want to align the number of holidays among employees.
* One of the two designated people must come to work.


※I used a translation tool to translate the English text.(https://www.deepl.com/translator)
