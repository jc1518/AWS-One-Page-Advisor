#!/usr/bin/env python3
"""
    AWS One Page Advisor
    Author: Jackie Chen (support@jackiechen.org)
    Version: 2018-02-19
"""

import config
import os
import awssupport
from json2html import *
import webbrowser


color = {
    'error': '<font color=#ff000>error</font>',
    'ok': '<font color=#32cd32>ok</font>',
    'warning': '<font color=#ffA500>warning</font>',
    'not_available': '<font color=#808080>not_available</font>'
    }


def get_all_checks(profile):
    """Retrieve Checks ID"""
    service_limits = {}
    fault_tolerance = {}
    cost_optimizing = {}
    security = {}
    performance = {}
    support_client = awssupport.Client(profile)

    def categorize_check(checktype, check):
        checktype[check['id']] = {
            'name': check['name'],
            'description': check['description'],
            'metadata': check['metadata']
        }
    checks = support_client.describe_checks()

    for check in checks['checks']:
        if check['category'] == 'service_limits':
            categorize_check(service_limits, check)
        if check['category'] == 'fault_tolerance':
            categorize_check(fault_tolerance, check)
        if check['category'] == 'cost_optimizing':
            categorize_check(cost_optimizing, check)
        if check['category'] == 'security':
            categorize_check(security, check)
        if check['category'] == 'performance':
            categorize_check(performance, check)
    all_checks = {
        'service_limits': service_limits,
        'fault_tolerance': fault_tolerance,
        'cost_optimizing': cost_optimizing,
        'security': security,
        'performance': performance
    }
    return all_checks


def get_check_summary(check_ids):
    support_client = awssupport.Client(profile)
    check_summary = support_client.checks_summary(check_ids)
    return check_summary


def build_report(index, profile, category, report):
    print('>>>>>>>>>>>>> Checking', category ,'in AWS account', profile)
    report.append({'Account': profile})
    category_check = get_all_checks(profile)[category]
    category_check_summary = get_check_summary(list(category_check.keys()))
    for check in category_check_summary['summaries']:
        print(category_check[check['checkId']]['name'], ':', check['status'])
        report[index][category_check[check['checkId']]['name']] = color[check['status']]

if __name__ == '__main__':
    security_check_report = []
    performance_check_report = []
    service_limits_check_report = []
    fault_tolerance_check_report = []
    cost_optimizing_check_report = []
    n = 0
    for profile in config.profiles:
        for category in config.categories:
            if category == 'security':
                build_report(n, profile, category, security_check_report)
            if category == 'performance':
                build_report(n, profile, category, performance_check_report)
            if category == 'service_limits':
                build_report(n, profile, category, service_limits_check_report)
            if category == 'fault_tolerance':
                build_report(n, profile, category, fault_tolerance_check_report)
            if category == 'cost_optimizing':
                build_report(n, profile, category, cost_optimizing_check_report)
        n += 1

    for category in config.categories:
        if category == 'security':
            # Security report
            with open('security_check_report.html', 'w') as f:
                f.write(json2html.convert(json=security_check_report, escape=False))
            webbrowser.open('file://' + os.path.realpath('security_check_report.html'))
        if category == 'performance':
            # Performance report
            with open('performance_check_report.html', 'w') as f:
                f.write(json2html.convert(json=performance_check_report, escape=False))
            webbrowser.open('file://' + os.path.realpath('performance_check_report.html'))
        if category == 'service_limits':
            # Service limit
            with open('service_limits_check_report.html', 'w') as f:
                f.write(json2html.convert(json=service_limits_check_report, escape=False))
            webbrowser.open('file://' + os.path.realpath('service_limits_check_report.html'))
        if category == 'fault_tolerance':
            # Fault tolerance
            with open('fault_tolerance_check_report.html', 'w') as f:
                f.write(json2html.convert(json=fault_tolerance_check_report, escape=False))
            webbrowser.open('file://' + os.path.realpath('fault_tolerance_check_report.html'))
        if category == 'cost_optimizing':
            # Cost optimizing
            with open('cost_optimizing_check_report.html', 'w') as f:
                f.write(json2html.convert(json=cost_optimizing_check_report, escape=False))
            webbrowser.open('file://' + os.path.realpath('cost_optimizing_check_report.html'))