#!/bin/bash
awk -f transform.awk -F "|" $1
